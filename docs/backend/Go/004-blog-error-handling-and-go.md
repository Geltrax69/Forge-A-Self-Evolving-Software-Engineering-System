url: https://go.dev/blog/error-handling-and-go
----

# Error handling and Go

## Introduction

If you have written any Go code you have probably encountered the built-in `error` type. Go code uses `error` values to indicate an abnormal state. For example, the `os.Open` function returns a non-nil `error` value when it fails to open a file.

```go
func Open(name string) (file *File, err error)
```

The following code uses `os.Open` to open a file. If an error occurs it calls `log.Fatal` to print the error message and stop.

```go
f, err := os.Open("filename.ext")
if err != nil {
    log.Fatal(err)
}
// do something with the open *File f
```

## The error type

The `error` type is an interface type. An `error` variable represents any value that can describe itself as a string. Here is the interface's declaration:

```go
type error interface {
    Error() string
}
```

The most commonly-used `error` implementation is the errors package's unexported `errorString` type.

```go
// errorString is a trivial implementation of error.
type errorString struct {
    s string
}

func (e *errorString) Error() string {
    return e.s
}
```

You can construct one of these values with the `errors.New` function:

```go
// New returns an error that formats as the given text.
func New(text string) error {
    return &errorString{text}
}
```

Usage:

```go
func Sqrt(f float64) (float64, error) {
    if f < 0 {
        return 0, errors.New("math: square root of negative number")
    }
    // implementation
}
```

The `fmt` package formats an `error` value by calling its `Error() string` method. It is the error implementation's responsibility to summarize the context, e.g. "open /etc/passwd: permission denied," not just "permission denied."

`fmt.Errorf` formats a string according to `Printf`'s rules and returns it as an `error`:

```go
if f < 0 {
    return 0, fmt.Errorf("math: square root of negative number %g", f)
}
```

Since `error` is an interface, you can use arbitrary data structures as error values so callers can inspect details:

```go
type NegativeSqrtError float64

func (f NegativeSqrtError) Error() string {
    return fmt.Sprintf("math: square root of negative number %g", float64(f))
}
```

A sophisticated caller can use a type assertion to check for a specific error type and handle it specially, while callers that just pass the error to `fmt.Println` or `log.Fatal` see no change in behavior. Example from the `json` package:

```go
type SyntaxError struct {
    msg    string // description of error
    Offset int64  // error occurred after reading Offset bytes
}

func (e *SyntaxError) Error() string { return e.msg }
```

```go
if err := dec.Decode(&val); err != nil {
    if serr, ok := err.(*json.SyntaxError); ok {
        line, col := findLine(f, serr.Offset)
        return fmt.Errorf("%s:%d:%d: %v", f.Name(), line, col, err)
    }
    return err
}
```

Specific error implementations might have additional methods, e.g. `net.Error`:

```go
package net

type Error interface {
    error
    Timeout() bool   // Is the error a timeout?
    Temporary() bool // Is the error temporary?
}
```

```go
if nerr, ok := err.(net.Error); ok && nerr.Temporary() {
    time.Sleep(1e9)
    continue
}
if err != nil {
    log.Fatal(err)
}
```

## Simplifying repetitive error handling

In Go, error handling is important: the design and conventions encourage explicitly checking for errors where they occur, rather than throwing/catching exceptions. This can make code verbose, but there are techniques to reduce repetition.

Consider an HTTP handler that retrieves a record and formats it with a template — each handler duplicating identical error-response code:

```go
func viewRecord(w http.ResponseWriter, r *http.Request) {
    c := appengine.NewContext(r)
    key := datastore.NewKey(c, "Record", r.FormValue("id"), 0, nil)
    record := new(Record)
    if err := datastore.Get(c, key, record); err != nil {
        http.Error(w, err.Error(), 500)
        return
    }
    if err := viewTemplate.Execute(w, record); err != nil {
        http.Error(w, err.Error(), 500)
    }
}
```

Define a custom handler type that returns an `error`:

```go
type appHandler func(http.ResponseWriter, *http.Request) error
```

Simplify the handler to just return errors:

```go
func viewRecord(w http.ResponseWriter, r *http.Request) error {
    c := appengine.NewContext(r)
    key := datastore.NewKey(c, "Record", r.FormValue("id"), 0, nil)
    record := new(Record)
    if err := datastore.Get(c, key, record); err != nil {
        return err
    }
    return viewTemplate.Execute(w, record)
}
```

Implement `http.Handler` on `appHandler` so the http package can use it:

```go
func (fn appHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    if err := fn(w, r); err != nil {
        http.Error(w, err.Error(), 500)
    }
}
```

Register with `http.Handle` (not `HandleFunc`):

```go
func init() {
    http.Handle("/view", appHandler(viewRecord))
}
```

To give friendlier messages while logging full errors, wrap richer context in a custom error struct:

```go
type appError struct {
    Error   error
    Message string
    Code    int
}

type appHandler func(http.ResponseWriter, *http.Request) *appError

func (fn appHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    if e := fn(w, r); e != nil {
        c := appengine.NewContext(r)
        c.Errorf("%v", e.Error)
        http.Error(w, e.Message, e.Code)
    }
}

func viewRecord(w http.ResponseWriter, r *http.Request) *appError {
    c := appengine.NewContext(r)
    key := datastore.NewKey(c, "Record", r.FormValue("id"), 0, nil)
    record := new(Record)
    if err := datastore.Get(c, key, record); err != nil {
        return &appError{err, "Record not found", 404}
    }
    if err := viewTemplate.Execute(w, record); err != nil {
        return &appError{err, "Can't display record", 500}
    }
    return nil
}
```

Further ideas: give the error handler a pretty HTML template, write stack traces to the response for admins, store the stack trace at error-construction time, and recover from panics inside `appHandler`, logging "Critical" while telling the user "a serious error has occurred."

## Conclusion

Proper error handling is an essential requirement of good software. Using these techniques you can write more reliable and succinct Go code.

----
