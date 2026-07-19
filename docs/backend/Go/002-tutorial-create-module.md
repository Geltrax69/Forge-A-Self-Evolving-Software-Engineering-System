url: https://go.dev/doc/tutorial/create-module
----

# Tutorial: Create a Go module

This is the first part of a tutorial that introduces a few fundamental features of the Go language. If you're just getting started with Go, be sure to take a look at "Tutorial: Get started with Go", which introduces the `go` command, Go modules, and very simple Go code.

In this tutorial you'll create two modules. The first is a library which is intended to be imported by other libraries or applications. The second is a caller application which will use the first.

This tutorial's sequence includes seven brief topics that each illustrate a different part of the language:

1. Create a module -- Write a small module with functions you can call from another module.
2. Call your code from another module -- Import and use your new module.
3. Return and handle an error -- Add simple error handling.
4. Return a random greeting -- Handle data in slices (Go's dynamically-sized arrays).
5. Return greetings for multiple people -- Store key/value pairs in a map.
6. Add a test -- Use Go's built-in unit testing features to test your code.
7. Compile and install the application -- Compile and install your code locally.

## Prerequisites

- **Some programming experience.** The code here is pretty simple, but it helps to know something about functions, loops, and arrays.
- **Go.** We recommend using the latest version of Go to follow this tutorial.
- **A tool to edit your code.** Any text editor works; popular choices include VSCode, GoLand, and Vim.
- **A command terminal.** Go works well using any terminal on Linux and Mac, and on PowerShell or cmd in Windows.

## Start a module that others can use

Start by creating a Go module. In a module, you collect one or more related packages for a discrete and useful set of functions.

Go code is grouped into packages, and packages are grouped into modules. Your module specifies dependencies needed to run your code, including the Go version and the set of other modules it requires.

As you add or improve functionality in your module, you publish new versions of the module. Developers writing code that calls functions in your module can import the module's updated packages and test with the new version before putting it into production use.

### Step 1: Open a command prompt and cd to your home directory

On Linux or Mac:
```
cd
```

On Windows:
```
cd %HOMEPATH%
```

### Step 2: Create a greetings directory for your Go module source code

```
mkdir greetings
cd greetings
```

### Step 3: Start your module using the go mod init command

Run the `go mod init` command, giving it your module path -- here, use `example.com/greetings`. If you publish a module, this _must_ be a path from which your module can be downloaded by Go tools (i.e. your code's repository).

```
$ go mod init example.com/greetings
go: creating new go.mod: module example.com/greetings
```

The `go mod init` command creates a go.mod file to track your code's dependencies. So far, the file includes only the name of your module and the Go version your code supports. But as you add dependencies, the go.mod file will list the versions your code depends on. This keeps builds reproducible and gives you direct control over which module versions to use.

### Step 4: Create a greetings.go file

In your text editor, create a file in which to write your code and call it greetings.go.

### Step 5: Write your code

Paste the following code into your greetings.go file and save the file.

```go
package greetings

import "fmt"

// Hello returns a greeting for the named person.
func Hello(name string) string {
    // Return a greeting that embeds the name in a message.
    message := fmt.Sprintf("Hi, %v. Welcome!", name)
    return message
}
```

This is the first code for your module. It returns a greeting to any caller that asks for one.

In this code, you:

- **Declare a `greetings` package** to collect related functions.
- **Implement a `Hello` function** to return the greeting. This function takes a `name` parameter whose type is `string`. The function also returns a `string`. In Go, a function whose name starts with a capital letter can be called by a function not in the same package — an exported name.
- **Declare a `message` variable** to hold your greeting. In Go, the `:=` operator is a shortcut for declaring and initializing a variable in one line (Go uses the value on the right to determine the variable's type). The long way:

  ```go
  var message string
  message = fmt.Sprintf("Hi, %v. Welcome!", name)
  ```

- **Use the `fmt` package's `Sprintf` function** to create a greeting message, substituting the `name` parameter's value for the `%v` format verb.
- **Return the formatted greeting text** to the caller.

## Next steps

In the next step, you'll call this function from another module ("Call your code from another module").

----
