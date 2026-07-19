url: https://go.dev/ref/mod
----

# Go Modules Reference

## Introduction

Modules are how Go manages dependencies.

This document is a detailed reference manual for Go's module system. For an introduction to creating Go projects, see [How to Write Go Code](/doc/code.html). For information on using modules, migrating projects to modules, and other topics, see the blog series starting with [Using Go Modules](/blog/using-go-modules).

## Modules, packages, and versions

A module is a collection of packages that are released, versioned, and distributed together. Modules may be downloaded directly from version control repositories or from module proxy servers.

A module is identified by a [module path](#glos-module-path), which is declared in a [`go.mod` file](#go-mod-file), together with information about the module's dependencies. The module root directory is the directory that contains the `go.mod` file. The main module is the module containing the directory where the `go` command is invoked.

Each package within a module is a collection of source files in the same directory that are compiled together. A package path is the module path joined with the subdirectory containing the package (relative to the module root). For example, the module `"golang.org/x/net"` contains a package in the directory `"html"`. That package's path is `"golang.org/x/net/html"`.

### Module paths

A module path is the canonical name for a module, declared with the [`module` directive](#go-mod-file-module) in the module's [`go.mod` file](#glos-go-mod-file). A module's path is the prefix for package paths within the module.

A module path should describe both what the module does and where to find it. Typically, a module path consists of a repository root path, a directory within the repository (usually empty), and a major version suffix (only for major version 2 or higher).

- The repository root path is the portion of the module path that corresponds to the root directory of the version control repository where the module is developed. Most modules are defined in their repository's root directory, so this is usually the entire path. For example, `golang.org/x/net` is the repository root path for the module of the same name. See [Finding a repository for a module path](#vcs-find) for information on how the `go` command locates a repository using HTTP requests derived from a module path.
- If the module is not defined in the repository's root directory, the module subdirectory is the part of the module path that names the directory, not including the major version suffix. This also serves as a prefix for semantic version tags. For example, the module `golang.org/x/tools/gopls` is in the `gopls` subdirectory of the repository with root path `golang.org/x/tools`, so it has the module subdirectory `gopls`. See [Mapping versions to commits](#vcs-version) and [Module directories within a repository](#vcs-dir).
- If the module is released at major version 2 or higher, the module path must end with a [major version suffix](#major-version-suffixes) like `/v2`. This may or may not be part of the subdirectory name. For example, the module with path `golang.org/x/repo/sub/v2` could be in the `/sub` or `/sub/v2` subdirectory of the repository `golang.org/x/repo`.

If a module might be depended on by other modules, these rules must be followed so that the `go` command can find and download the module. There are also several [lexical restrictions](#go-mod-file-ident) on characters allowed in module paths.

A module that will never be fetched as a dependency of any other module may use any valid package path for its module path, but must take care not to collide with paths that may be used by the module's dependencies or the Go standard library. The Go standard library uses package paths that do not contain a dot in the first path element, and the `go` command does not attempt to resolve such paths from network servers. The paths `example` and `test` are reserved for users: they will not be used in the standard library and are suitable for use in self-contained modules, such as those defined in tutorials or example code or created and manipulated as part of a test.

### Versions

A version identifies an immutable snapshot of a module, which may be either a [release](#glos-release-version) or a [pre-release](#glos-pre-release-version). Each version starts with the letter `v`, followed by a semantic version. See [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) for details on how versions are formatted, interpreted, and compared.

To summarize, a semantic version consists of three non-negative integers (the major, minor, and patch versions, from left to right) separated by dots. The patch version may be followed by an optional pre-release string starting with a hyphen. The pre-release string or patch version may be followed by a build metadata string starting with a plus. For example, `v0.0.0`, `v1.12.134`, `v8.0.5-pre`, and `v2.0.9+meta` are valid versions.

Each part of a version indicates whether the version is stable and whether it is compatible with previous versions.

- The [major version](#glos-major-version) must be incremented and the minor and patch versions must be set to zero after a backwards incompatible change is made to the module's public interface or documented functionality, for example, after a package is removed.
- The [minor version](#glos-minor-version) must be incremented and the patch version set to zero after a backwards compatible change, for example, after a new function is added.
- The [patch version](#glos-patch-version) must be incremented after a change that does not affect the module's public interface, such as a bug fix or optimization.
- The pre-release suffix indicates a version is a [pre-release](#glos-pre-release-version). Pre-release versions sort before the corresponding release versions. For example, `v1.2.3-pre` comes before `v1.2.3`.
- The build metadata suffix is ignored for the purpose of comparing versions. The go command accepts versions with build metadata and converts them to pseudo-versions to maintain the total ordering between versions.
  - The special suffix `+incompatible` denotes a version released before migrating to modules version major version 2 or later (see [Compatibility with non-module repositories](#non-module-compat)).
  - The special suffix `+dirty` is appended to the version information of a binary when it's built with a Go toolchain 1.24 or later within a valid local Version Control System (VCS) repository that contains uncommitted changes in the working directory.

A version is considered unstable if its major version is 0 or it has a pre-release suffix. Unstable versions are not subject to compatibility requirements. For example, `v0.2.0` may not be compatible with `v0.1.0`, and `v1.5.0-beta` may not be compatible with `v1.5.0`.

Go may access modules in version control systems using tags, branches, or revisions that don't follow these conventions. However, within the main module, the `go` command will automatically convert revision names that don't follow this standard into canonical versions. The `go` command will also remove build metadata suffixes (except for `+incompatible`) as part of this process. This may result in a [pseudo-version](#glos-pseudo-version), a pre-release version that encodes a revision identifier (such as a Git commit hash) and a timestamp from a version control system. For example, the command `go get golang.org/x/net@daa7c041` will convert the commit hash `daa7c041` into the pseudo-version `v0.0.0-20191109021931-daa7c04131f5`. Canonical versions are required outside the main module, and the `go` command will report an error if a non-canonical version like `master` appears in a `go.mod` file.

### Pseudo-versions

A pseudo-version is a specially formatted [pre-release](#glos-pre-release-version) [version](#glos-version) that encodes information about a specific revision in a version control repository. For example, `v0.0.0-20191109021931-daa7c04131f5` is a pseudo-version.

Pseudo-versions may refer to revisions for which no [semantic version tags](#glos-semantic-version-tag) are available. They may be used to test commits before creating version tags, for example, on a development branch.

Each pseudo-version has three parts:

- A base version prefix (`vX.0.0` or `vX.Y.Z-0`), which is either derived from a semantic version tag that precedes the revision or `vX.0.0` if there is no such tag.
- A timestamp (`yyyymmddhhmmss`), which is the UTC time the revision was created. In Git, this is the commit time, not the author time.
- A revision identifier (`abcdefabcdef`), which is a 12-character prefix of the commit hash, or in Subversion, a zero-padded revision number.

Each pseudo-version may be in one of three forms, depending on the base version. These forms ensure that a pseudo-version compares higher than its base version, but lower than the next tagged version.

- `vX.0.0-yyyymmddhhmmss-abcdefabcdef` is used when there is no known base version. As with all versions, the major version `X` must match the module's [major version suffix](#glos-major-version-suffix).
- `vX.Y.Z-pre.0.yyyymmddhhmmss-abcdefabcdef` is used when the base version is a pre-release version like `vX.Y.Z-pre`.
- `vX.Y.(Z+1)-0.yyyymmddhhmmss-abcdefabcdef` is used when the base version is a release version like `vX.Y.Z`. For example, if the base version is `v1.2.3`, a pseudo-version might be `v1.2.4-0.20191109021931-daa7c04131f5`.

More than one pseudo-version may refer to the same commit by using different base versions. This happens naturally when a lower version is tagged after a pseudo-version is written.

These forms give pseudo-versions two useful properties:

- Pseudo-versions with known base versions sort higher than those versions but lower than other pre-release for later versions.
- Pseudo-versions with the same base version prefix sort chronologically.

The `go` command performs several checks to ensure that module authors have control over how pseudo-versions are compared with other versions and that pseudo-versions refer to revisions that are actually part of a module's commit history.

- If a base version is specified, there must be a corresponding semantic version tag that is an ancestor of the revision described by the pseudo-version. This prevents developers from bypassing [minimal version selection](#glos-minimal-version-selection) using a pseudo-version that compares higher than all tagged versions like `v1.999.999-99999999999999-daa7c04131f5`.
- The timestamp must match the revision's timestamp. This prevents attackers from flooding [module proxies](#glos-module-proxy) with an unbounded number of otherwise identical pseudo-versions. This also prevents module consumers from changing the relative ordering of versions.
- The revision must be an ancestor of one of the module repository's branches or tags. This prevents attackers from referring to unapproved changes or pull requests.

Pseudo-versions never need to be typed by hand. Many commands accept a commit hash or a branch name and will translate it into a pseudo-version (or tagged version if available) automatically. For example:

```
go get example.com/mod@master
go list -m -json example.com/mod@abcd1234
```

### Major version suffixes

Starting with major version 2, module paths must have a major version suffix like `/v2` that matches the major version. For example, if a module has the path `example.com/mod` at `v1.0.0`, it must have the path `example.com/mod/v2` at version `v2.0.0`.

Major version suffixes implement the [import compatibility rule](https://research.swtch.com/vgo-import):

> If an old package and a new package have the same import path, the new package must be backwards compatible with the old package.

By definition, packages in a new major version of a module are not backwards compatible with the corresponding packages in the previous major version. Consequently, starting with `v2`, packages need new import paths. This is accomplished by adding a major version suffix to the module path. Since the module path is a prefix of the import path for each package within the module, adding the major version suffix to the module path provides a distinct import path for each incompatible version.

Major version suffixes are not allowed at major versions `v0` or `v1`. There is no need to change the module path between `v0` and `v1` because `v0` versions are unstable and have no compatibility guarantee. Additionally, for most modules, `v1` is backwards compatible with the last `v0` version; a `v1` version acts as a commitment to compatibility, rather than an indication of incompatible changes compared with `v0`.

As a special case, modules paths starting with `gopkg.in/` must always have a major version suffix, even at `v0` and `v1`. The suffix must start with a dot rather than a slash (for example, `gopkg.in/yaml.v2`).

Major version suffixes let multiple major versions of a module coexist in the same build. This may be necessary due to a [diamond dependency problem](https://research.swtch.com/vgo-import#dependency_story). Ordinarily, if a module is required at two different versions by transitive dependencies, the higher version will be used. However, if the two versions are incompatible, neither version will satisfy all clients. Since incompatible versions must have different major version numbers, they must also have different module paths due to major version suffixes. This resolves the conflict: modules with distinct suffixes are treated as separate modules, and their packages—even packages in same subdirectory relative to their module roots—are distinct.

Many Go projects released versions at `v2` or higher without using a major version suffix before migrating to modules (perhaps before modules were even introduced). These versions are annotated with a `+incompatible` build tag (for example, `v2.0.0+incompatible`). See [Compatibility with non-module repositories](#non-module-compat) for more information.

### Resolving a package to a module

When the `go` command loads a package using a [package path](#glos-package-path), it needs to determine which module provides the package.

The `go` command starts by searching the [build list](#glos-build-list) for modules with paths that are prefixes of the package path. For example, if the package `example.com/a/b` is imported, and the module `example.com/a` is in the build list, the `go` command will check whether `example.com/a` contains the package, in the directory `b`. At least one file with the `.go` extension must be present in a directory for it to be considered a package. [Build constraints](/pkg/go/build/#hdr-Build_Constraints) are not applied for this purpose. If exactly one module in the build list provides the package, that module is used. If no modules provide the package or if two or more modules provide the package, the `go` command reports an error. The `-mod=mod` flag instructs the `go` command to attempt to find new modules providing missing packages and to update `go.mod` and `go.sum`. The [`go get`](#go-get) and [`go mod tidy`](#go-mod-tidy) commands do this automatically.

When the `go` command looks up a new module for a package path, it checks the `GOPROXY` environment variable, which is a comma-separated list of proxy URLs or the keywords `direct` or `off`. A proxy URL indicates the `go` command should contact a [module proxy](#glos-module-proxy) using the [`GOPROXY` protocol](#goproxy-protocol). `direct` indicates that the `go` command should [communicate with a version control system](#vcs). `off` indicates that no communication should be attempted. The `GOPRIVATE` and `GONOPROXY` [environment variables](#environment-variables) can also be used to control this behavior.

For each entry in the `GOPROXY` list, the `go` command requests the latest version of each module path that might provide the package (that is, each prefix of the package path). For each successfully requested module path, the `go` command will download the module at the latest version and check whether the module contains the requested package. If one or more modules contain the requested package, the module with the longest path is used. If one or more modules are found but none contain the requested package, an error is reported. If no modules are found, the `go` command tries the next entry in the `GOPROXY` list. If no entries are left, an error is reported.

For example, suppose the `go` command is looking for a module that provides the package `golang.org/x/net/html`, and `GOPROXY` is set to `https://corp.example.com,https://proxy.golang.org`. The `go` command may make the following requests:

- To `https://corp.example.com/` (in parallel):
  - Request for latest version of `golang.org/x/net/html`
  - Request for latest version of `golang.org/x/net`
  - Request for latest version of `golang.org/x`
  - Request for latest version of `golang.org`
- To `https://proxy.golang.org/`, if all requests to `https://corp.example.com/` have failed with 404 or 410:
  - Request for latest version of `golang.org/x/net/html`
  - Request for latest version of `golang.org/x/net`
  - Request for latest version of `golang.org/x`
  - Request for latest version of `golang.org`

After a suitable module has been found, the `go` command will add a new [requirement](#go-mod-file-require) with the new module's path and version to the main module's `go.mod` file. This ensures that when the same package is loaded in the future, the same module will be used at the same version. If the resolved package is not imported by a package in the main module, the new requirement will have an `// indirect` comment.

## `go.mod` files

A module is defined by a UTF-8 encoded text file named `go.mod` in its root directory. The `go.mod` file is line-oriented. Each line holds a single directive, made up of a keyword followed by arguments. For example:

```
module example.com/my/thing

go 1.23.0

require example.com/other/thing v1.0.2
require example.com/new/thing/v2 v2.3.4
exclude example.com/old/thing v1.2.3
replace example.com/bad/thing v1.4.5 => example.com/good/thing v1.4.5
retract [v1.9.0, v1.9.5]
```

The leading keyword can be factored out of adjacent lines to create a block, like in Go imports.

```
require (
    example.com/new/thing/v2 v2.3.4
    example.com/old/thing v1.2.3
)
```

The `go.mod` file is designed to be human readable and machine writable. The `go` command provides several subcommands that change `go.mod` files. For example, [`go get`](#go-get) can upgrade or downgrade specific dependencies. Commands that load the module graph will [automatically update](#go-mod-file-updates) `go.mod` when needed. [`go mod edit`](#go-mod-edit) can perform low-level edits. The [`golang.org/x/mod/modfile`](https://pkg.go.dev/golang.org/x/mod/modfile?tab=doc) package can be used by Go programs to make the same changes programmatically.

A `go.mod` file is required for the [main module](#glos-main-module), and for any [replacement module](#go-mod-file-replace) specified with a local file path. However, a module that lacks an explicit `go.mod` file may still be [required](#go-mod-file-require) as a dependency, or used as a replacement specified with a module path and version; see [Compatibility with non-module repositories](#non-module-compat).

### Lexical elements

When a `go.mod` file is parsed, its content is broken into a sequence of tokens. There are several kinds of tokens: whitespace, comments, punctuation, keywords, identifiers, and strings.

_White space_ consists of spaces (U+0020), tabs (U+0009), carriage returns (U+000D), and newlines (U+000A). White space characters other than newlines have no effect except to separate tokens that would otherwise be combined. Newlines are significant tokens.

_Comments_ start with `//` and run to the end of a line. `/* */` comments are not allowed.

_Punctuation_ tokens include `(`, `)`, and `=>`.

_Keywords_ distinguish different kinds of directives in a `go.mod` file. Allowed keywords are `module`, `go`, `require`, `replace`, `exclude`, and `retract`.

_Identifiers_ are sequences of non-whitespace characters, such as module paths or semantic versions.

_Strings_ are quoted sequences of characters. There are two kinds of strings: interpreted strings beginning and ending with quotation marks (`"`, U+0022) and raw strings beginning and ending with grave accents (`` ` ``, U+0060). Interpreted strings may contain escape sequences consisting of a backslash (`\`, U+005C) followed by another character. An escaped quotation mark (`\"`) does not terminate an interpreted string. The unquoted value of an interpreted string is the sequence of characters between quotation marks with each escape sequence replaced by the character following the backslash (for example, `\"` is replaced by `"`, `\n` is replaced by `n`). In contrast, the unquoted value of a raw string is simply the sequence of characters between grave accents; backslashes have no special meaning within raw strings.

Identifiers and strings are interchangeable in the `go.mod` grammar.

### Module paths and versions

Most identifiers and strings in a `go.mod` file are either module paths or versions.

A module path must satisfy the following requirements:

- The path must consist of one or more path elements separated by slashes (`/`, U+002F). It must not begin or end with a slash.
- Each path element is a non-empty string made of up ASCII letters, ASCII digits, and limited ASCII punctuation (`-`, `.`, `_`, and `~`).
- A path element may not begin or end with a dot (`.`, U+002E).
- The element prefix up to the first dot must not be a reserved file name on Windows, regardless of case (`CON`, `com1`, `NuL`, and so on).
- The element prefix up to the first dot must not end with a tilde followed by one or more digits (like `EXAMPL~1.COM`).

If the module path appears in a `require` directive and is not replaced, or if the module paths appears on the right side of a `replace` directive, the `go` command may need to download modules with that path, and some additional requirements must be satisfied.

- The leading path element (up to the first slash, if any), by convention a domain name, must contain only lower-case ASCII letters, ASCII digits, dots (`.`, U+002E), and dashes (`-`, U+002D); it must contain at least one dot and cannot start with a dash.
- For a final path element of the form `/vN` where `N` looks numeric (ASCII digits and dots), `N` must not begin with a leading zero, must not be `/v1`, and must not contain any dots.
  - For paths beginning with `gopkg.in/`, this requirement is replaced by a requirement that the path follow the [gopkg.in](https://gopkg.in) service's conventions.

Versions in `go.mod` files may be [canonical](#glos-canonical-version) or non-canonical.

A canonical version starts with the letter `v`, followed by a semantic version following the [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) specification. See [Versions](#versions) for more information.

Most other identifiers and strings may be used as non-canonical versions, though there are some restrictions to avoid problems with file systems, repositories, and [module proxies](#glos-module-proxy). Non-canonical versions are only allowed in the main module's `go.mod` file. The `go` command will attempt to replace each non-canonical version with an equivalent canonical version when it automatically [updates](#go-mod-file-updates) the `go.mod` file.

In places where a module path is associated with a version (as in `require`, `replace`, and `exclude` directives), the final path element must be consistent with the version. See [Major version suffixes](#major-version-suffixes).

### Grammar

`go.mod` syntax is specified below using Extended Backus-Naur Form (EBNF). See the [Notation section in the Go Language Specification](/ref/spec#Notation) for details on EBNF syntax.

```
GoMod = { Directive } .
Directive = ModuleDirective |
            GoDirective |
            ToolDirective |
            IgnoreDirective |
            RequireDirective |
            ExcludeDirective |
            ReplaceDirective |
            RetractDirective .
```

Newlines, identifiers, and strings are denoted with `newline`, `ident`, and `string`, respectively.

Module paths and versions are denoted with `ModulePath` and `Version`.

```
ModulePath = ident | string . /* see restrictions above */
Version = ident | string .    /* see restrictions above */
```

### `module` directive

A `module` directive defines the main module's [path](#glos-module-path). A `go.mod` file must contain exactly one `module` directive.

```
ModuleDirective = "module" ( ModulePath | "(" newline ModulePath newline ")" ) newline .
```

Example:

```
module golang.org/x/net
```

#### Deprecation

A module can be marked as deprecated in a block of comments containing the string `Deprecated:` (case-sensitive) at the beginning of a paragraph. The deprecation message starts after the colon and runs to the end of the paragraph. The comments may appear immediately before the `module` directive or afterward on the same line.

Example:

```
// Deprecated: use example.com/mod/v2 instead.
module example.com/mod
```

Since Go 1.17, [`go list -m -u`](#go-list-m) checks for information on all deprecated modules in the [build list](#glos-build-list). [`go get`](#go-get) checks for deprecated modules needed to build packages named on the command line.

When the `go` command retrieves deprecation information for a module, it loads the `go.mod` file from the version matching the `@latest` [version query](#version-queries) without considering [retractions](#go-mod-file-retract) or [exclusions](#go-mod-file-exclude). The `go` command loads the list of [retracted versions](#glos-retracted-version) from the same `go.mod` file.

To deprecate a module, an author may add a `// Deprecated:` comment and tag a new release. The author may change or remove the deprecation message in a higher release.

A deprecation applies to all minor versions of a module. Major versions higher than `v2` are considered separate modules for this purpose, since their [major version suffixes](#glos-major-version-suffix) give them distinct module paths.

Deprecation messages are intended to inform users that the module is no longer supported and to provide migration instructions, for example, to the latest major version. Individual minor and patch versions cannot be deprecated; [`retract`](#go-mod-file-retract) may be more appropriate for that.

### `go` directive

A `go` directive indicates that a module was written assuming the semantics of a given version of Go. The version must be a valid [Go version](/doc/toolchain#version), such as `1.14`, `1.21rc1`, or `1.23.0`.

The `go` directive sets the minimum version of Go required to use this module. Before Go 1.21, the directive was advisory only; now it is a mandatory requirement: Go toolchains refuse to use modules declaring newer Go versions.

The `go` directive is an input into selecting which Go toolchain to run. See "[Go toolchains](/doc/toolchain)" for details.

The `go` directive affects use of new language features:

- For packages within the module, the compiler rejects use of language features introduced after the version specified by the `go` directive. For example, if a module has the directive `go 1.12`, its packages may not use numeric literals like `1_000_000`, which were introduced in Go 1.13.
- If an older Go version builds one of the module's packages and encounters a compile error, the error notes that the module was written for a newer Go version. For example, suppose a module has `go 1.13` and a package uses the numeric literal `1_000_000`. If that package is built with Go 1.12, the compiler notes that the code is written for Go 1.13.

The `go` directive also affects the behavior of the `go` command:

- At `go 1.14` or higher, automatic [vendoring](#vendoring) may be enabled. If the file `vendor/modules.txt` is present and consistent with `go.mod`, there is no need to explicitly use the `-mod=vendor` flag.
- At `go 1.16` or higher, the `all` package pattern matches only packages transitively imported by packages and tests in the [main module](#glos-main-module). This is the same set of packages retained by [`go mod vendor`](#go-mod-vendor) since modules were introduced. In lower versions, `all` also includes tests of packages imported by packages in the main module, tests of those packages, and so on.
- At `go 1.17` or higher:
  - The `go.mod` file includes an explicit [`require` directive](#go-mod-file-require) for each module that provides any package transitively imported by a package or test in the main module. (At `go 1.16` and lower, an [indirect dependency](#glos-direct-dependency) is included only if [minimal version selection](#minimal-version-selection) would otherwise select a different version.) This extra information enables [module graph pruning](#graph-pruning) and [lazy module loading](#lazy-loading).
  - Because there may be many more `// indirect` dependencies than in previous `go` versions, indirect dependencies are recorded in a separate block within the `go.mod` file.
  - `go mod vendor` omits `go.mod` and `go.sum` files for vendored dependencies. (That allows invocations of the `go` command within subdirectories of `vendor` to identify the correct main module.)
  - `go mod vendor` records the `go` version from each dependency's `go.mod` file in `vendor/modules.txt`.
- At `go 1.21` or higher:
  - The `go` line declares a required minimum version of Go to use with this module.
  - The `go` line must be greater than or equal to the `go` line of all dependencies.
  - The `go` command no longer attempts to maintain compatibility with the previous older version of Go.
  - The `go` command is more careful about keeping checksums of `go.mod` files in the `go.sum` file.

A `go.mod` file may contain at most one `go` directive. Most commands will add a `go` directive with the current Go version if one is not present.

If the `go` directive is missing, `go 1.16` is assumed.

```
GoDirective = "go" GoVersion newline .
GoVersion = string | ident .  /* valid release version; see above */
```

Example:

```
go 1.23.0
```

### `toolchain` directive

A `toolchain` directive declares a suggested Go toolchain to use with a module. The suggested Go toolchain's version cannot be less than the required Go version declared in the `go` directive. The `toolchain` directive only has an effect when the module is the main module and the default toolchain's version is less than the suggested toolchain's version.

For reproducibility, the `go` command writes its own toolchain name in a `toolchain` line any time it is updating the `go` version in the `go.mod` file (usually during `go get`).

For details, see "[Go toolchains](/doc/toolchain)".

```
ToolchainDirective = "toolchain" ToolchainName newline .
ToolchainName = string | ident .  /* valid toolchain name; see "Go toolchains" */
```

Example:

```
toolchain go1.21.0
```

### `godebug` directive

A `godebug` directive declares a single [GODEBUG setting](/doc/godebug) to apply when this module is the main module. There can be more than one such line, and they can be factored. It is an error for the main module to name a GODEBUG key that does not exist. The effect of `godebug key=value` is as if every main package being compiled contained a source file that listed `//go:debug key=value`.

```
GodebugDirective = "godebug" ( GodebugSpec | "(" newline { GodebugSpec } ")" newline ) .
GodebugSpec = GodebugKey "=" GodebugValue newline.
GodebugKey = GodebugChar { GodebugChar }.
GodebugValue = GodebugChar { GodebugChar }.
GodebugChar = any non-space character except , " ` ' (comma and quotes).
```

Example:

```
godebug default=go1.21
godebug (
    panicnil=1
    asynctimerchan=0
)
```

### `require` directive

A `require` directive declares a minimum required version of a given module dependency. For each required module version, the `go` command loads the `go.mod` file for that version and incorporates the requirements from that file. Once all requirements have been loaded, the `go` command resolves them using [minimal version selection (MVS)](#minimal-version-selection) to produce the [build list](#glos-build-list).

The `go` command automatically adds `// indirect` comments for some requirements. An `// indirect` comment indicates that no package from the required module is directly imported by any package in the [main module](#glos-main-module).

If the [`go` directive](#go-mod-file-go) specifies `go 1.16` or lower, the `go` command adds an indirect requirement when the selected version of a module is higher than what is already implied (transitively) by the main module's other dependencies. That may occur because of an explicit upgrade (`go get -u ./...`), removal of some other dependency that previously imposed the requirement (`go mod tidy`), or a dependency that imports a package without a corresponding requirement in its own `go.mod` file (such as a dependency that lacks a `go.mod` file altogether).

At `go 1.17` and above, the `go` command adds an indirect requirement for each module that provides any package imported (even [indirectly](#glos-indirect-dependency)) by a package or test in the main module or passed as an argument to `go get`. These more comprehensive requirements enable [module graph pruning](#graph-pruning) and [lazy module loading](#lazy-loading).

```
RequireDirective = "require" ( RequireSpec | "(" newline { RequireSpec } ")" newline ) .
RequireSpec = ModulePath Version newline .
```

Example:

```
require golang.org/x/net v1.2.3

require (
    golang.org/x/crypto v1.4.5 // indirect
    golang.org/x/text v1.6.7
)
```

### `tool` directive

Since Go 1.24, a `tool` directive adds a package as a dependency of the current module. It also makes it available to run with `go tool` when the current working directory is within this module, or within a workspace that contains this module.

If the tool package is not in the current module, a `require` directive must be present that specifies the version of the tool to use.

The `tool` meta-pattern resolves to the list of tools defined in the current module's `go.mod`, or in workspace mode to the union of all tools defined in all modules in the workspace.

```
ToolDirective = "tool" ( ToolSpec | "(" newline { ToolSpec } ")" newline ) .
ToolSpec = ModulePath newline .
```

Example:

```
tool golang.org/x/tools/cmd/stringer

tool (
    example.com/module/cmd/a
    example.com/module/cmd/b
)
```

### `ignore` directive

An `ignore` directive will cause the go command ignore the slash-separated directory paths, and any files or directories recursively contained in them, when matching package patterns.

If the path starts with `./`, the path is interpreted relative to the module root directory, and that directory and any directories or files recursively contained in it will be ignored when matching package patterns.

Otherwise, any directories with the path at any depth in the module, and any directories or files recursively contained in them will be ignored.

```
IgnoreDirective = "ignore" ( IgnoreSpec | "(" newline { IgnoreSpec } ")" newline ) .
IgnoreSpec = RelativeFilePath newline .
RelativeFilePath = /* slash-separated relative file path */ .
```

Example

```
ignore ./node_modules

ignore (
    static
    content/html
    ./third_party/javascript
)
```

### `exclude` directive

An `exclude` directive prevents a module version from being loaded by the `go` command.

Since Go 1.16, if a version referenced by a `require` directive in any `go.mod` file is excluded by an `exclude` directive in the main module's `go.mod` file, the requirement is ignored. This may cause commands like [`go get`](#go-get) and [`go mod tidy`](#go-mod-tidy) to add new requirements on higher versions to `go.mod`, with an `// indirect` comment if appropriate.

Before Go 1.16, if an excluded version was referenced by a `require` directive, the `go` command listed available versions for the module (as shown with [`go list -m -versions`](#go-list-m)) and loaded the next higher non-excluded version instead. This could result in non-deterministic version selection, since the next higher version could change over time. Both release and pre-release versions were considered for this purpose, but pseudo-versions were not. If there were no higher versions, the `go` command reported an error.

`exclude` directives only apply in the main module's `go.mod` file and are ignored in other modules. See [Minimal version selection](#minimal-version-selection) for details.

```
ExcludeDirective = "exclude" ( ExcludeSpec | "(" newline { ExcludeSpec } ")" newline ) .
ExcludeSpec = ModulePath Version newline .
```

Example:

```
exclude golang.org/x/net v1.2.3

exclude (
    golang.org/x/crypto v1.4.5
    golang.org/x/text v1.6.7
)
```

### `replace` directive

A `replace` directive replaces the contents of a specific version of a module, or all versions of a module, with contents found elsewhere. The replacement may be specified with either another module path and version, or a platform-specific file path.

If a version is present on the left side of the arrow (`=>`), only that specific version of the module is replaced; other versions will be accessed normally. If the left version is omitted, all versions of the module are replaced.

If the path on the right side of the arrow is an absolute or relative path (beginning with `./` or `../`), it is interpreted as the local file path to the replacement module root directory, which must contain a `go.mod` file. The replacement version must be omitted in this case.

If the path on the right side is not a local path, it must be a valid module path. In this case, a version is required. The same module version must not also appear in the build list.

Regardless of whether a replacement is specified with a local path or module path, if the replacement module has a `go.mod` file, its `module` directive must match the module path it replaces.

`replace` directives only apply in the main module's `go.mod` file and are ignored in other modules. See [Minimal version selection](#minimal-version-selection) for details.

If there are multiple main modules, all main modules' `go.mod` files apply. Conflicting `replace` directives across main modules are disallowed, and must be removed or overridden in a [replace in the `go.work file`](#go-work-file-replace).

Note that a `replace` directive alone does not add a module to the [module graph](#glos-module-graph). A [`require` directive](#go-mod-file-require) that refers to a replaced module version is also needed, either in the main module's `go.mod` file or a dependency's `go.mod` file. A `replace` directive has no effect if the module version on the left side is not required.

```
ReplaceDirective = "replace" ( ReplaceSpec | "(" newline { ReplaceSpec } ")" newline ) .
ReplaceSpec = ModulePath [ Version ] "=>" FilePath newline
            | ModulePath [ Version ] "=>" ModulePath Version newline .
FilePath = /* platform-specific relative or absolute file path */
```

Example:

```
replace golang.org/x/net v1.2.3 => example.com/fork/net v1.4.5

replace (
    golang.org/x/net v1.2.3 => example.com/fork/net v1.4.5
    golang.org/x/net => example.com/fork/net v1.4.5
    golang.org/x/net v1.2.3 => ./fork/net
    golang.org/x/net => ./fork/net
)
```

### `retract` directive

A `retract` directive indicates that a version or range of versions of the module defined by `go.mod` should not be depended upon. A `retract` directive is useful when a version was published prematurely or a severe problem was discovered after the version was published. Retracted versions should remain available in version control repositories and on [module proxies](#glos-module-proxy) to ensure that builds that depend on them are not broken. The word _retract_ is borrowed from academic literature: a retracted research paper is still available, but it has problems and should not be the basis of future work.

When a module version is retracted, users will not upgrade to it automatically using [`go get`](#go-get), [`go mod tidy`](#go-mod-tidy), or other commands. Builds that depend on retracted versions should continue to work, but users will be notified of retractions when they check for updates with [`go list -m -u`](#go-list-m) or update a related module with [`go get`](#go-get).

To retract a version, a module author should add a `retract` directive to `go.mod`, then publish a new version containing that directive. The new version must be higher than other release or pre-release versions; that is, the `@latest` [version query](#version-queries) should resolve to the new version before retractions are considered. The `go` command loads and applies retractions from the version shown by `go list -m -retracted $modpath@latest` (where `$modpath` is the module path).

Retracted versions are hidden from the version list printed by [`go list -m -versions`](#go-list-m) unless the `-retracted` flag is used. Retracted versions are excluded when resolving version queries like `@>=v1.2.3` or `@latest`.

A version containing retractions may retract itself. If the highest release or pre-release version of a module retracts itself, the `@latest` query resolves to a lower version after retracted versions are excluded.

As an example, consider a case where the author of module `example.com/m` publishes version `v1.0.0` accidentally. To prevent users from upgrading to `v1.0.0`, the author can add two `retract` directives to `go.mod`, then tag `v1.0.1` with the retractions.

```
retract (
    v1.0.0 // Published accidentally.
    v1.0.1 // Contains retractions only.
)
```

When a user runs `go get example.com/m@latest`, the `go` command reads retractions from `v1.0.1`, which is now the highest version. Both `v1.0.0` and `v1.0.1` are retracted, so the `go` command will upgrade (or downgrade!) to the next highest version, perhaps `v0.9.5`.

`retract` directives may be written with either a single version (like `v1.0.0`) or with a closed interval of versions with an upper and lower bound, delimited by `[` and `]` (like `[v1.1.0, v1.2.0]`). A single version is equivalent to an interval where the upper and lower bound are the same. Like other directives, multiple `retract` directives may be grouped together in a block delimited by `(` at the end of a line and `)` on its own line.

Each `retract` directive should have a comment explaining the rationale for the retraction, though this is not mandatory. The `go` command may display rationale comments in warnings about retracted versions and in `go list` output. A rationale comment may be written immediately above a `retract` directive (without a blank line in between) or afterward on the same line. If a comment appears above a block, it applies to all `retract` directives within the block that don't have their own comments. A rationale comment may span multiple lines.

```
RetractDirective = "retract" ( RetractSpec | "(" newline { RetractSpec } ")" newline ) .
RetractSpec = ( Version | "[" Version "," Version "]" ) newline .
```

Examples:

- Retracting all versions between `v1.0.0` and `v1.9.9`:

```
retract v1.0.0
retract [v1.0.0, v1.9.9]
retract (
    v1.0.0
    [v1.0.0, v1.9.9]
)
```

- Returning to unversioned after prematurely released a version `v1.0.0`:

```
retract [v0.0.0, v1.0.1] // assuming v1.0.1 contains this retraction.
```

- Wiping out a module including all pseudo-versions and tagged versions:

```
retract [v0.0.0-0, v0.15.2]  // assuming v0.15.2 contains this retraction.
```

The `retract` directive was added in Go 1.16. Go 1.15 and lower will report an error if a `retract` directive is written in the [main module's](#glos-main-module) `go.mod` file and will ignore `retract` directives in `go.mod` files of dependencies.

### Automatic updates

Most commands report an error if `go.mod` is missing information or doesn't accurately reflect reality. The [`go get`](#go-get) and [`go mod tidy`](#go-mod-tidy) commands may be used to fix most of these problems. Additionally, the `-mod=mod` flag may be used with most module-aware commands (`go build`, `go test`, and so on) to instruct the `go` command to fix problems in `go.mod` and `go.sum` automatically.

For example, consider this `go.mod` file:

```
module example.com/M

go 1.23.0

require (
    example.com/A v1
    example.com/B v1.0.0
    example.com/C v1.0.0
    example.com/D v1.2.3
    example.com/E dev
)

exclude example.com/D v1.2.3
```

The update triggered with `-mod=mod` rewrites non-canonical version identifiers to [canonical](#glos-canonical-version) semver form, so `example.com/A`'s `v1` becomes `v1.0.0`, and `example.com/E`'s `dev` becomes the pseudo-version for the latest commit on the `dev` branch, perhaps `v0.0.0-20180523231146-b3f5c0f6e5f1`.

The update modifies requirements to respect exclusions, so the requirement on the excluded `example.com/D v1.2.3` is updated to use the next available version of `example.com/D`, perhaps `v1.2.4` or `v1.3.0`.

The update removes redundant or misleading requirements. For example, if `example.com/A v1.0.0` itself requires `example.com/B v1.2.0` and `example.com/C v1.0.0`, then `go.mod`'s requirement of `example.com/B v1.0.0` is misleading (superseded by `example.com/A`'s need for `v1.2.0`), and its requirement of `example.com/C v1.0.0` is redundant (implied by `example.com/A`'s need for the same version), so both will be removed. If the main module contains packages that directly import packages from `example.com/B` or `example.com/C`, then the requirements will be kept but updated to the actual versions being used.

Finally, the update reformats the `go.mod` in a canonical formatting, so that future mechanical changes will result in minimal diffs. The `go` command will not update `go.mod` if only formatting changes are needed.

Because the module graph defines the meaning of import statements, any commands that load packages also use `go.mod` and can therefore update it, including `go build`, `go get`, `go install`, `go list`, `go test`, `go mod tidy`.

In Go 1.15 and lower, the `-mod=mod` flag was enabled by default, so updates were performed automatically. Since Go 1.16, the `go` command acts as if `-mod=readonly` were set instead: if any changes to `go.mod` are needed, the `go` command reports an error and suggests a fix.

## Minimal version selection (MVS)

Go uses an algorithm called Minimal version selection (MVS) to select a set of module versions to use when building packages. MVS is described in detail in [Minimal Version Selection](https://research.swtch.com/vgo-mvs) by Russ Cox.

Conceptually, MVS operates on a directed graph of modules, specified with [`go.mod` files](#glos-go-mod-file). Each vertex in the graph represents a module version. Each edge represents a minimum required version of a dependency, specified using a [`require`](#go-mod-file-require) directive. The graph may be modified by [`exclude`](#go-mod-file-exclude) and [`replace`](#go-mod-file-replace) directives in the `go.mod` file(s) of the main module(s) and by [`replace`](#go-work-file-replace) directives in the `go.work` file.

MVS produces the [build list](#glos-build-list) as output, the list of module versions used for a build.

MVS starts at the main modules (special vertices in the graph that have no version) and traverses the graph, tracking the highest required version of each module. At the end of the traversal, the highest required versions comprise the build list: they are the minimum versions that satisfy all requirements.

The build list may be inspected with the command [`go list -m all`](#go-list-m). Unlike other dependency management systems, the build list is not saved in a "lock" file. MVS is deterministic, and the build list doesn't change when new versions of dependencies are released, so MVS is used to compute it at the beginning of every module-aware command.

Consider the example in the diagram below. The main module requires module A at version 1.2 or higher and module B at version 1.2 or higher. A 1.2 and B 1.2 require C 1.3 and C 1.4, respectively. C 1.3 and C 1.4 both require D 1.2.

MVS visits and loads the `go.mod` file for each of the module versions highlighted in blue. At the end of the graph traversal, MVS returns a build list containing the bolded versions: A 1.2, B 1.2, C 1.4, and D 1.2. Note that higher versions of B and D are available but MVS does not select them, since nothing requires them.

### Replacement

The content of a module (including its `go.mod` file) may be replaced using a [`replace` directive](#go-mod-file-replace) in a main module's `go.mod` file or a workspace's `go.work` file. A `replace` directive may apply to a specific version of a module or to all versions of a module.

Replacements change the module graph, since a replacement module may have different dependencies than replaced versions.

Consider the example below, where C 1.4 has been replaced with R. R depends on D 1.3 instead of D 1.2, so MVS returns a build list containing A 1.2, B 1.2, C 1.4 (replaced with R), and D 1.3.

### Exclusion

A module may also be excluded at specific versions using an [`exclude` directive](#go-mod-file-exclude) in the main module's `go.mod` file.

Exclusions also change the module graph. When a version is excluded, it is removed from the module graph, and requirements on it are redirected to the next higher version.

Consider the example below. C 1.3 has been excluded. MVS will act as if A 1.2 required C 1.4 (the next higher version) instead of C 1.3.

### Upgrades

The [`go get`](#go-get) command may be used to upgrade a set of modules. To perform an upgrade, the `go` command changes the module graph before running MVS by adding edges from visited versions to upgraded versions.

Consider the example below. Module B may be upgraded from 1.2 to 1.3, C may be upgraded from 1.3 to 1.4, and D may be upgraded from 1.2 to 1.3.

Upgrades (and downgrades) may add or remove indirect dependencies. In this case, E 1.1 and F 1.1 appear in the build list after the upgrade, since E 1.1 is required by B 1.3.

To preserve upgrades, the `go` command updates the requirements in `go.mod`. It will change the requirement on B to version 1.3. It will also add requirements on C 1.4 and D 1.3 with `// indirect` comments, since those versions would not be selected otherwise.

### Downgrade

The [`go get`](#go-get) command may also be used to downgrade a set of modules. To perform a downgrade, the `go` command changes the module graph by removing versions above the downgraded versions. It also removes versions of other modules that depend on removed versions, since they may not be compatible with the downgraded versions of their dependencies. If the main module requires a module version removed by downgrading, the requirement is changed to a previous version that has not been removed. If no previous version is available, the requirement is dropped.

Consider the example below. Suppose that a problem was found with C 1.4, so we downgrade to C 1.3. C 1.4 is removed from the module graph. B 1.2 is also removed, since it requires C 1.4 or higher. The main module's requirement on B is changed to 1.1.

[`go get`](#go-get) can also remove dependencies entirely, using an `@none` suffix after an argument. This works similarly to a downgrade. All versions of the named module are removed from the module graph.

## Module graph pruning

If the main module is at `go 1.17` or higher, the [module graph](#glos-module-graph) used for [minimal version selection](#minimal-version-selection) includes only the _immediate_ requirements for each module dependency that specifies `go 1.17` or higher in its own `go.mod` file, unless that version of the module is also (transitively) required by some _other_ dependency at `go 1.16` or below. (The _transitive_ dependencies of `go 1.17` dependencies are _pruned out_ of the module graph.)

Since a `go 1.17` `go.mod` file includes a [require directive](#go-mod-file-require) for every dependency needed to build any package or test in that module, the pruned module graph includes all of the dependencies needed to `go build` or `go test` the packages in any dependency explicitly required by the [main module](#glos-main-module). A module that is _not_ needed to build any package or test in a given module cannot affect the run-time behavior of its packages, so the dependencies that are pruned out of the module graph would only cause interference between otherwise-unrelated modules.

Modules whose requirements have been pruned out still appear in the module graph and are still reported by `go list -m all`: their [selected versions](#glos-selected-version) are known and well-defined, and packages can be loaded from those modules (for example, as transitive dependencies of tests loaded from other modules). However, since the `go` command cannot easily identify which dependencies of these modules are satisfied, the arguments to `go build` and `go test` cannot include packages from modules whose requirements have been pruned out. [`go get`](#go-get) promotes the module containing each named package to an explicit dependency, allowing `go build` or `go test` to be invoked on that package.

Because Go 1.16 and earlier did not support module graph pruning, the full transitive closure of dependencies — including transitive `go 1.17` dependencies — is still included for each module that specifies `go 1.16` or lower. (At `go 1.16` and below, the `go.mod` file includes only [direct dependencies](#glos-direct-dependency), so a much larger graph must be loaded to ensure that all indirect dependencies are included.)

The [`go.sum` file](#go-sum-files) recorded by [`go mod tidy`](#go-mod-tidy) for a module by default includes checksums needed by the Go version _one below_ the version specified in its [`go` directive](#go-mod-file-go). So a `go 1.17` module includes checksums needed for the full module graph loaded by Go 1.16, but a `go 1.18` module will include only the checksums needed for the pruned module graph loaded by Go 1.17. The `-compat` flag can be used to override the default version (for example, to prune the `go.sum` file more aggressively in a `go 1.17` module).

See [the design document](https://go.googlesource.com/proposal/+/master/design/36460-lazy-module-loading.md) for more detail.

### Lazy module loading

The more comprehensive requirements added for module graph pruning also enable another optimization when working within a module. If the main module is at `go 1.17` or higher, the `go` command avoids loading the complete module graph until (and unless) it is needed. Instead, it loads only the main module's `go.mod` file, then attempts to load the packages to be built using only those requirements. If a package to be imported (for example, a dependency of a test for a package outside the main module) is not found among those requirements, then the rest of the module graph is loaded on demand.

If all imported packages can be found without loading the module graph, the `go` command then loads the `go.mod` files for _only_ the modules containing those packages, and their requirements are checked against the requirements of the main module to ensure that they are locally consistent. (Inconsistencies can arise due to version-control merges, hand-edits, and changes in modules that have been [replaced](#go-mod-file-replace) using local filesystem paths.)

## Workspaces

A workspace is a collection of modules on disk that are used as the main modules when running [minimal version selection (MVS)](#minimal-version-selection).

A workspace can be declared in a [`go.work` file](#go-work-file) that specifies relative paths to the module directories of each of the modules in the workspace. When no `go.work` file exists, the workspace consists of the single module containing the current directory.

Most `go` subcommands that work with modules operate on the set of modules determined by the current workspace. `go mod init`, `go mod why`, `go mod edit`, `go mod tidy`, `go mod vendor`, and `go get` always operate on a single main module.

A command determines whether it is in a workspace context by first examining the `GOWORK` environment variable. If `GOWORK` is set to `off`, the command will be in a single-module context. If it is empty or not provided, the command will search the current working directory, and then successive parent directories, for a file `go.work`. If a file is found, the command will operate in the workspace it defines; otherwise, the workspace will include only the module containing the working directory. If `GOWORK` names a path to an existing file that ends in .work, workspace mode will be enabled. Any other value is an error. You can use the `go env GOWORK` command to determine which `go.work` file the `go` command is using. `go env GOWORK` will be empty if the `go` command is not in workspace mode.

### `go.work` files

A workspace is defined by a UTF-8 encoded text file named `go.work`. The `go.work` file is line oriented. Each line holds a single directive, made up of a keyword followed by arguments. For example:

```
go 1.23.0

use ./my/first/thing
use ./my/second/thing

replace example.com/bad/thing v1.4.5 => example.com/good/thing v1.4.5
```

As in `go.mod` files, a leading keyword can be factored out of adjacent lines to create a block.

```
use (
    ./my/first/thing
    ./my/second/thing
)
```

The `go` command provides several subcommands for manipulating `go.work` files. [`go work init`](#go-work-init) creates new `go.work` files. [`go work use`](#go-work-use) adds module directories to the `go.work` file. [`go work edit`](#go-work-edit) performs low-level edits. The [`golang.org/x/mod/modfile`](https://pkg.go.dev/golang.org/x/mod/modfile?tab=doc) package can be used by Go programs to make the same changes programmatically.

The go command will maintain a `go.work.sum` file that keeps track of hashes used by the workspace that are not in collective workspace modules' go.sum files.

It is generally inadvisable to commit go.work files into version control systems, for two reasons:

- A checked-in `go.work` file might override a developer's own `go.work` file from a parent directory, causing confusion when their `use` directives don't apply.
- A checked-in `go.work` file may cause a continuous integration (CI) system to select and thus test the wrong versions of a module's dependencies. CI systems should generally not be allowed to use the `go.work` file so that they can test the behavior of the module as it would be used when required by other modules, where a `go.work` file within the module has no effect.

That said, there are some cases where committing a `go.work` file makes sense. For example, when the modules in a repository are developed exclusively with each other but not together with external modules, there may not be a reason the developer would want to use a different combination of modules in a workspace. In that case, the module author should ensure the individual modules are tested and released properly.

### Lexical elements

Lexical elements in `go.work` files are defined in exactly the same way [as for `go.mod files`](#go-mod-file-lexical).

### Grammar

`go.work` syntax is specified below using Extended Backus-Naur Form (EBNF). See the [Notation section in the Go Language Specification](/ref/spec#Notation) for details on EBNF syntax.

```
GoWork = { Directive } .
Directive = GoDirective |
            ToolchainDirective |
            UseDirective |
            ReplaceDirective .
```

Newlines, identifiers, and strings are denoted with `newline`, `ident`, and `string`, respectively.

Module paths and versions are denoted with `ModulePath` and `Version`. Module paths and versions are specified in exactly the same way [as for `go.mod files`](#go-mod-file-lexical).

```
ModulePath = ident | string . /* see restrictions above */
Version = ident | string .    /* see restrictions above */
```

### `go` directive

A `go` directive is required in a valid `go.work` file. The version must be a valid Go release version: a positive integer followed by a dot and a non-negative integer (for example, `1.18`, `1.19`).

The `go` directive indicates the go toolchain version with which the `go.work` file is intended to work. If changes are made to the `go.work` file format, future versions of the toolchain will interpret the file according to its indicated version.

A `go.work` file may contain at most one `go` directive.

```
GoDirective = "go" GoVersion newline .
GoVersion = string | ident .  /* valid release version; see above */
```

Example:

```
go 1.23.0
```

### `toolchain` directive

A `toolchain` directive declares a suggested Go toolchain to use in a workspace. It only has an effect when the default toolchain is older than the suggested toolchain.

For details, see "[Go toolchains](/doc/toolchain)".

```
ToolchainDirective = "toolchain" ToolchainName newline .
ToolchainName = string | ident .  /* valid toolchain name; see "Go toolchains" */
```

Example:

```
toolchain go1.21.0
```

### `godebug` directive

A `godebug` directive declares a single [GODEBUG setting](/doc/godebug) to apply when working in this workspace. The syntax and effect is the same as the [`go.mod` file's `godebug` directive](#go-mod-file-godebug). When a workspace is in use, `godebug` directives in `go.mod` files are ignored.

### `use` directive

A `use` adds a module on disk to the set of main modules in a workspace. Its argument is a relative path to the directory containing the module's `go.mod` file. A `use` directive does not add modules contained in subdirectories of its argument directory. Those modules may be added by the directory containing their `go.mod` file in separate `use` directives.

```
UseDirective = "use" ( UseSpec | "(" newline { UseSpec } ")" newline ) .
UseSpec = FilePath newline .
FilePath = /* platform-specific relative or absolute file path */
```

Example:

```
use ./mymod  // example.com/mymod

use (
    ../othermod
    ./subdir/thirdmod
)
```

### `replace` directive

Similar to a `replace` directive in a `go.mod` file, a `replace` directive in a `go.work` file replaces the contents of a specific version of a module, or all versions of a module, with contents found elsewhere. A wildcard replace in `go.work` overrides a version-specific `replace` in a `go.mod` file.

`replace` directives in `go.work` files override any replaces of the same module or module version in workspace modules.

```
ReplaceDirective = "replace" ( ReplaceSpec | "(" newline { ReplaceSpec } ")" newline ) .
ReplaceSpec = ModulePath [ Version ] "=>" FilePath newline
            | ModulePath [ Version ] "=>" ModulePath Version newline .
FilePath = /* platform-specific relative or absolute file path */
```

Example:

```
replace golang.org/x/net v1.2.3 => example.com/fork/net v1.4.5

replace (
    golang.org/x/net v1.2.3 => example.com/fork/net v1.4.5
    golang.org/x/net => example.com/fork/net v1.4.5
    golang.org/x/net v1.2.3 => ./fork/net
    golang.org/x/net => ./fork/net
)
```

## Compatibility with non-module repositories

To ensure a smooth transition from `GOPATH` to modules, the `go` command can download and build packages in module-aware mode from repositories that have not migrated to modules by adding a [`go.mod` file](#glos-go-mod-file).

When the `go` command downloads a module at a given version [directly](#vcs) from a repository, it looks up a repository URL for the module path, maps the version to a revision within the repository, then extracts an archive of the repository at that revision. If the [module's path](#glos-module-path) is equal to the [repository root path](#glos-repository-root-path), and the repository root directory does not contain a `go.mod` file, the `go` command synthesizes a `go.mod` file in the module cache that contains a [`module` directive](#go-mod-file-module) and nothing else. Since synthetic `go.mod` files do not contain [`require` directives](#go-mod-file-require) for their dependencies, other modules that depend on them may need additional `require` directives (with `// indirect` comments) to ensure each dependency is fetched at the same version on every build.

When the `go` command downloads a module from a [proxy](#communicating-with-proxies), it downloads the `go.mod` file separately from the rest of the module content. The proxy is expected to serve a synthetic `go.mod` file if the original module didn't have one.

### `+incompatible` versions

A module released at major version 2 or higher must have a matching [major version suffix](#major-version-suffixes) on its module path. For example, if a module is released at `v2.0.0`, its path must have a `/v2` suffix. This allows the `go` command to treat multiple major versions of a project as distinct modules, even if they're developed in the same repository.

The major version suffix requirement was introduced when module support was added to the `go` command, and many repositories had already tagged releases with major version `2` or higher before that. To maintain compatibility with these repositories, the `go` command adds an `+incompatible` suffix to versions with major version 2 or higher without a `go.mod` file. `+incompatible` indicates that a version is part of the same module as versions with lower major version numbers; consequently, the `go` command may automatically upgrade to higher `+incompatible` versions even though it may break the build.

Consider the example requirement below:

```
require example.com/m v4.1.2+incompatible
```

The version `v4.1.2+incompatible` refers to the [semantic version tag](#glos-semantic-version-tag) `v4.1.2` in the repository that provides the module `example.com/m`. The module must be in the repository root directory (that is, the [repository root path](#glos-module-path) must also be `example.com/m`), and a `go.mod` file must not be present. The module may have versions with lower major version numbers like `v1.5.2`, and the `go` command may upgrade automatically to `v4.1.2+incompatible` from those versions (see [minimal version selection (MVS)](#minimal-version-selection) for information on how upgrades work).

A repository that migrates to modules after version `v2.0.0` is tagged should usually release a new major version. In the example above, the author should create a module with the path `example.com/m/v5` and should release version `v5.0.0`. The author should also update imports of packages in the module to use the prefix `example.com/m/v5` instead of `example.com/m`. See [Go Modules: v2 and Beyond](/blog/v2-go-modules) for a more detailed example.

Note that the `+incompatible` suffix should not appear on a tag in a repository; a tag like `v4.1.2+incompatible` will be ignored. The suffix only appears in versions used by the `go` command. See [Mapping versions to commits](#vcs-version) for details on the distinction between versions and tags.

Note also that the `+incompatible` suffix may appear on [pseudo-versions](#glos-pseudo-version). For example, `v2.0.1-20200722182040-012345abcdef+incompatible` may be a valid pseudo-version.

### Minimal module compatibility

A module released at major version 2 or higher is required to have a [major version suffix](#glos-major-version-suffix) on its [module path](#glos-module-path). The module may or may not be developed in a [major version subdirectory](#glos-major-version-subdirectory) within its repository. This has implications for packages that import packages within the module when building `GOPATH` mode.

Normally in `GOPATH` mode, a package is stored in a directory matching its [repository's root path](#glos-repository-root-path) joined with its directory within the repository. For example, a package in the repository with root path `example.com/repo` in the subdirectory `sub` would be stored in `$GOPATH/src/example.com/repo/sub` and would be imported as `example.com/repo/sub`.

For a module with a major version suffix, one might expect to find the package `example.com/repo/v2/sub` in the directory `$GOPATH/src/example.com/repo/v2/sub`. This would require the module to be developed in the `v2` subdirectory of its repository. The `go` command supports this but does not require it (see [Mapping versions to commits](#vcs-version)).

If a module is _not_ developed in a major version subdirectory, then its directory in `GOPATH` will not contain the major version suffix, and its packages may be imported without the major version suffix. In the example above, the package would be found in the directory `$GOPATH/src/example.com/repo/sub` and would be imported as `example.com/repo/sub`.

This creates a problem for packages intended to be built in both module mode and `GOPATH` mode: module mode requires a suffix, while `GOPATH` mode does not.

To fix this, minimal module compatibility was added in Go 1.11 and was backported to Go 1.9.7 and 1.10.3. When an import path is resolved to a directory in `GOPATH` mode:

- When resolving an import of the form `$modpath/$vn/$dir` where:
  - `$modpath` is a valid module path,
  - `$vn` is a major version suffix,
  - `$dir` is a possibly empty subdirectory,
- If all of the following are true:
  - The package `$modpath/$vn/$dir` is not present in any relevant [`vendor` directory](#glos-vendor-directory).
  - A `go.mod` file is present in the same directory as the importing file or in any parent directory up to the `$GOPATH/src` root,
  - No `$GOPATH[i]/src/$modpath/$vn/$suffix` directory exists (for any root `$GOPATH[i]`),
  - The file `$GOPATH[d]/src/$modpath/go.mod` exists (for some root `$GOPATH[d]`) and declares the module path as `$modpath/$vn`,
- Then the import of `$modpath/$vn/$dir` is resolved to the directory `$GOPATH[d]/src/$modpath/$dir`.

This rules allow packages that have been migrated to modules to import other packages that have been migrated to modules when built in `GOPATH` mode even when a major version subdirectory was not used.

## Module-aware commands

Most `go` commands may run in _Module-aware mode_ or _`GOPATH` mode_. In module-aware mode, the `go` command uses `go.mod` files to find versioned dependencies, and it typically loads packages out of the [module cache](#glos-module-cache), downloading modules if they are missing. In `GOPATH` mode, the `go` command ignores modules; it looks in [`vendor` directories](#glos-vendor-directory) and in `GOPATH` to find dependencies.

As of Go 1.16, module-aware mode is enabled by default, regardless of whether a `go.mod` file is present. In lower versions, module-aware mode was enabled when a `go.mod` file was present in the current directory or any parent directory.

Module-aware mode may be controlled with the `GO111MODULE` environment variable, which can be set to `on`, `off`, or `auto`.

- If `GO111MODULE=off`, the `go` command ignores `go.mod` files and runs in `GOPATH` mode.
- If `GO111MODULE=on` or is unset, the `go` command runs in module-aware mode, even when no `go.mod` file is present. Not all commands work without a `go.mod` file: see [Module commands outside a module](#commands-outside).
- If `GO111MODULE=auto`, the `go` command runs in module-aware mode if a `go.mod` file is present in the current directory or any parent directory. In Go 1.15 and lower, this was the default behavior. `go mod` subcommands and `go install` with a [version query](#version-queries) run in module-aware mode even if no `go.mod` file is present.

In module-aware mode, `GOPATH` no longer defines the meaning of imports during a build, but it still stores downloaded dependencies (in `GOPATH/pkg/mod`; see [Module cache](#module-cache)) and installed commands (in `GOPATH/bin`, unless `GOBIN` is set).

### Build commands

All commands that load information about packages are module-aware. This includes:

- `go build`
- `go fix`
- `go generate`
- `go install`
- `go list`
- `go run`
- `go test`
- `go vet`

When run in module-aware mode, these commands use `go.mod` files to interpret import paths listed on the command line or written in Go source files. These commands accept the following flags, common to all module commands.

- The `-mod` flag controls whether `go.mod` may be automatically updated and whether the `vendor` directory is used.
  - `-mod=mod` tells the `go` command to ignore the vendor directory and to [automatically update](#go-mod-file-updates) `go.mod`, for example, when an imported package is not provided by any known module.
  - `-mod=readonly` tells the `go` command to ignore the `vendor` directory and to report an error if `go.mod` needs to be updated.
  - `-mod=vendor` tells the `go` command to use the `vendor` directory. In this mode, the `go` command will not use the network or the module cache.
  - By default, if the [`go` version](#go-mod-file-go) in `go.mod` is `1.14` or higher and a `vendor` directory is present, the `go` command acts as if `-mod=vendor` were used. Otherwise, the `go` command acts as if `-mod=readonly` were used.
  - `go get` rejects this flag as the purpose of the command is to modify dependencies, which is only allowed by `-mod=mod`.
- The `-modcacherw` flag instructs the `go` command to create new directories in the module cache with read-write permissions instead of making them read-only. When this flag is used consistently (typically by setting `GOFLAGS=-modcacherw` in the environment or by running `go env -w GOFLAGS=-modcacherw`), the module cache may be deleted with commands like `rm -r` without changing permissions first. The [`go clean -modcache`](#go-clean-modcache) command may be used to delete the module cache, whether or not `-modcacherw` was used.
- The `-modfile=file.mod` flag instructs the `go` command to read (and possibly write) an alternate file instead of `go.mod` in the module root directory. The file's name must end with `.mod`. A file named `go.mod` must still be present in order to determine the module root directory, but it is not accessed. When `-modfile` is specified, an alternate `go.sum` file is also used: its path is derived from the `-modfile` flag by trimming the `.mod` extension and appending `.sum`.

### Vendoring

When using modules, the `go` command typically satisfies dependencies by downloading modules from their sources into the module cache, then loading packages from those downloaded copies. Vendoring may be used to allow interoperation with older versions of Go, or to ensure that all files used for a build are stored in a single file tree.

The [`go mod vendor`](#go-mod-vendor) command constructs a directory named `vendor` in the [main module's](#glos-main-module) root directory containing copies of all packages needed to build and test packages in the main module. Packages that are only imported by tests of packages outside the main module are not included. As with [`go mod tidy`](#go-mod-tidy) and other module commands, [build constraints](#glos-build-constraint) except for `ignore` are not considered when constructing the `vendor` directory.

`go mod vendor` also creates the file `vendor/modules.txt` that contains a list of vendored packages and the module versions they were copied from. When vendoring is enabled, this manifest is used as a source of module version information, as reported by [`go list -m`](#go-list-m) and [`go version -m`](#go-version-m). When the `go` command reads `vendor/modules.txt`, it checks that the module versions are consistent with `go.mod`. If `go.mod` has changed since `vendor/modules.txt` was generated, the `go` command will report an error. `go mod vendor` should be run again to update the `vendor` directory.

If the `vendor` directory is present in the main module's root directory, it will be used automatically if the [`go` version](#go-mod-file-go) in the main module's [`go.mod` file](#glos-go-mod-file) is `1.14` or higher. To explicitly enable vendoring, invoke the `go` command with the flag `-mod=vendor`. To disable vendoring, use the flag `-mod=readonly` or `-mod=mod`.

When vendoring is enabled, [build commands](#build-commands) like `go build` and `go test` load packages from the `vendor` directory instead of accessing the network or the local module cache. The [`go list -m`](#go-list-m) command only prints information about modules listed in `go.mod`. `go mod` commands such as [`go mod download`](#go-mod-download) and [`go mod tidy`](#go-mod-tidy) do not work differently when vendoring is enabled and will still download modules and access the module cache. [`go get`](#go-get) also does not work differently when vendoring is enabled.

Unlike [vendoring in `GOPATH` mode](/s/go15vendor), the `go` command ignores vendor directories in locations other than the main module's root directory. Additionally, since vendor directories in other modules are not used, the `go` command does not include vendor directories when building [module zip files](#zip-files) (but see known bugs [#31562](/issue/31562) and [#37397](/issue/37397)).

### `go get`

Usage:

```
go get [-d] [-t] [-u] [-tool] [build flags] [packages]
```

Examples:

```
# Upgrade a specific module.
$ go get golang.org/x/net

# Upgrade modules that provide packages imported by packages in the main module.
$ go get -u ./...

# Upgrade or downgrade to a specific version of a module.
$ go get golang.org/x/text@v0.3.2

# Update to the commit on the module's master branch.
$ go get golang.org/x/text@master

# Remove a dependency on a module and downgrade modules that require it
# to versions that don't require it.
$ go get golang.org/x/text@none

# Upgrade the minimum required Go version for the main module.
$ go get go

# Upgrade the suggested Go toolchain, leaving the minimum Go version alone.
$ go get toolchain

# Upgrade to the latest patch release of the suggested Go toolchain.
$ go get toolchain@patch
```

The `go get` command updates module dependencies in the [`go.mod` file](#go-mod-file) for the [main module](#glos-main-module), then builds and installs packages listed on the command line.

The first step is to determine which modules to update. `go get` accepts a list of packages, package patterns, and module paths as arguments. If a package argument is specified, `go get` updates the module that provides the package. If a package pattern is specified (for example, `all` or a path with a `...` wildcard), `go get` expands the pattern to a set of packages, then updates the modules that provide the packages. If an argument names a module but not a package (for example, the module `golang.org/x/net` has no package in its root directory), `go get` will update the module but will not build a package. If no arguments are specified, `go get` acts as if `.` were specified (the package in the current directory); this may be used together with the `-u` flag to update modules that provide imported packages.

Each argument may include a version query suffix indicating the desired version, as in `go get golang.org/x/text@v0.3.0`. A version query suffix consists of an `@` symbol followed by a [version query](#version-queries), which may indicate a specific version (`v0.3.0`), a version prefix (`v0.3`), a branch or tag name (`master`), a revision (`1234abcd`), or one of the special queries `latest`, `upgrade`, `patch`, or `none`. If no version is given, `go get` uses the `@upgrade` query.

Once `go get` has resolved its arguments to specific modules and versions, `go get` will add, change, or remove [`require` directives](#go-mod-file-require) in the main module's `go.mod` file to ensure the modules remain at the desired versions in the future. Note that required versions in `go.mod` files are _minimum versions_ and may be increased automatically as new dependencies are added. See [Minimal version selection (MVS)](#minimal-version-selection) for details on how versions are selected and conflicts are resolved by module-aware commands.

Other modules may be upgraded when a module named on the command line is added, upgraded, or downgraded if the new version of the named module requires other modules at higher versions. For example, suppose module `example.com/a` is upgraded to version `v1.5.0`, and that version requires module `example.com/b` at version `v1.2.0`. If module `example.com/b` is currently required at version `v1.1.0`, `go get example.com/a@v1.5.0` will also upgrade `example.com/b` to `v1.2.0`.

Other modules may be downgraded when a module named on the command line is downgraded or removed. To continue the above example, suppose module `example.com/b` is downgraded to `v1.1.0`. Module `example.com/a` would also be downgraded to a version that requires `example.com/b` at version `v1.1.0` or lower.

A module requirement may be removed using the version suffix `@none`. This is a special kind of downgrade. Modules that depend on the removed module will be downgraded or removed as needed. A module requirement may be removed even if one or more of its packages are imported by packages in the main module. In this case, the next build command may add a new module requirement.

If a module is needed at two different versions (specified explicitly in command line arguments or to satisfy upgrades and downgrades), `go get` will report an error.

After `go get` has selected a new set of versions, it checks whether any newly selected module versions or any modules providing packages named on the command line are [retracted](#glos-retracted-version) or [deprecated](#glos-deprecated-module). `go get` prints a warning for each retracted version or deprecated module it finds. [`go list -m -u all`](#go-list-m) may be used to check for retractions and deprecations in all dependencies.

After `go get` updates the `go.mod` file, it builds the packages named on the command line. Executables will be installed in the directory named by the `GOBIN` environment variable, which defaults to `$GOPATH/bin` or `$HOME/go/bin` if the `GOPATH` environment variable is not set.

`go get` supports the following flags:

- The `-d` flag tells `go get` not to build or install packages. When `-d` is used, `go get` will only manage dependencies in `go.mod`. Using `go get` without `-d` to build and install packages is deprecated (as of Go 1.17). In Go 1.18, `-d` will always be enabled.
- The `-u` flag tells `go get` to upgrade modules providing packages imported directly or indirectly by packages named on the command line. Each module selected by `-u` will be upgraded to its latest version unless it is already required at a higher version (a pre-release).
- The `-u=patch` flag (not `-u patch`) also tells `go get` to upgrade dependencies, but `go get` will upgrade each dependency to the latest patch version (similar to the `@patch` version query).
- The `-t` flag tells `go get` to consider modules needed to build tests of packages named on the command line. When `-t` and `-u` are used together, `go get` will update test dependencies as well.
- The `-insecure` flag should no longer be used. It permits `go get` to resolve custom import paths and fetch from repositories and module proxies using insecure schemes such as HTTP. The `GOINSECURE` [environment variable](#environment-variables) provides more fine-grained control and should be used instead.
- The `-tool` flag instructs go to add a matching tool line to `go.mod` for each listed package. If `-tool` is used with `@none`, the line will be removed.

Since Go 1.16, [`go install`](#go-install) is the recommended command for building and installing programs. When used with a version suffix (like `@latest` or `@v1.4.6`), `go install` builds packages in module-aware mode, ignoring the `go.mod` file in the current directory or any parent directory, if there is one.

`go get` is more focused on managing requirements in `go.mod`. The `-d` flag is deprecated, and since Go 1.18, it is always enabled.

### `go install`

Usage:

```
go install [build flags] [packages]
```

Examples:

```
# Install the latest version of a program,
# ignoring go.mod in the current directory (if any).
$ go install golang.org/x/tools/gopls@latest

# Install a specific version of a program.
$ go install golang.org/x/tools/gopls@v0.6.4

# Install a program at the version selected by the module in the current directory.
$ go install golang.org/x/tools/gopls

# Install all programs in a directory.
$ go install ./cmd/...
```

The `go install` command builds and installs the packages named by the paths on the command line. Executables (`main` packages) are installed to the directory named by the `GOBIN` environment variable, which defaults to `$GOPATH/bin` or `$HOME/go/bin` if the `GOPATH` environment variable is not set. Executables in `$GOROOT` are installed in `$GOROOT/bin` or `$GOTOOLDIR` instead of `$GOBIN`. Non-executable packages are built and cached but not installed.

Since Go 1.16, if the arguments have version suffixes (like `@latest` or `@v1.0.0`), `go install` builds packages in module-aware mode, ignoring the `go.mod` file in the current directory or any parent directory if there is one. This is useful for installing executables without affecting the dependencies of the main module.

To eliminate ambiguity about which module versions are used in the build, if any of the arguments have version suffixes, the arguments must satisfy the following constraints:

- Arguments must be package paths or package patterns (with "`...`" wildcards). They must not be standard packages (like `fmt`), meta-patterns (`std`, `cmd`, `all`, `work`, `tool`), or relative or absolute file paths. Note that `go install tool` can be used without a version suffix: see below.
- All arguments must have the same version suffix. Different queries are not allowed, even if they refer to the same version.
- All arguments must refer to packages in the same module at the same version.
- Package path arguments must refer to `main` packages. Pattern arguments will only match `main` packages.
- No module is considered the [main module](#glos-main-module).
  - If the module containing packages named on the command line has a `go.mod` file, it must not contain directives (`replace` and `exclude`) that would cause it to be interpreted differently if it were the main module.
  - The module must not require a higher version of itself.
  - Vendor directories are not used in any module. (Vendor directories are not included in [module zip files](#zip-files), so `go install` does not download them.)

See [Version queries](#version-queries) for supported version query syntax. Go 1.15 and lower did not support using version queries with `go install`.

If the arguments don't have version suffixes, `go install` may run in module-aware mode or `GOPATH` mode, depending on the `GO111MODULE` environment variable and the presence of a `go.mod` file. See [Module-aware commands](#mod-commands) for details. If module-aware mode is enabled, `go install` runs in the context of the main module, which may be different from the module containing the package being installed. In module-aware mode, `go install tool` can be used from a module to install all the tools in the module.

### `go tool`

Usage:

```
go tool [-n] command [args...]
```

Example:

```
$ go tool golang.org/x/tools/cmd/stringer
$ go tool stringer
```

In module mode, the `go tool` command can be used to build and run tools declared in `go.mod` files using a [`tool` directive](#go-mod-file-tool). The command can be specified using the full package path to a tool declared using a tool directive. The default binary name of the tool, which is the last component of the package path, excluding the major version suffix, can also be used if it is unique among installed tools.

### `go list -m`

Usage:

```
go list -m [-u] [-retracted] [-versions] [list flags] [modules]
```

Example:

```
$ go list -m all
$ go list -m -versions example.com/m
$ go list -m -json example.com/m@latest
```

The `-m` flag causes `go list` to list modules instead of packages. In this mode, the arguments to `go list` may be modules, module patterns (containing the `...` wildcard), [version queries](#version-queries), or the special pattern `all`, which matches all modules in the [build list](#glos-build-list). If no arguments are specified, the [main module](#glos-main-module) is listed.

When listing modules, the `-f` flag still specifies a format template applied to a Go struct, but now a `Module` struct:

```go
type Module struct {
    Path       string        // module path
    Version    string        // module version
    Versions   []string      // available module versions
    Replace    *Module       // replaced by this module
    Time       *time.Time    // time version was created
    Update     *Module       // available update (with -u)
    Main       bool          // is this the main module?
    Indirect   bool          // module is only indirectly needed by main module
    Dir        string        // directory holding local copy of files, if any
    GoMod      string        // path to go.mod file describing module, if any
    GoVersion  string        // go version used in module
    Retracted  []string      // retraction information, if any (with -retracted or -u)
    Deprecated string        // deprecation message, if any (with -u)
    Error      *ModuleError  // error loading module
}

type ModuleError struct {
    Err string // the error itself
}
```

The default output is to print the module path and then information about the version and replacement if any. For example, `go list -m all` might print:

```
example.com/main/module
golang.org/x/net v0.1.0
golang.org/x/text v0.3.0 => /tmp/text
rsc.io/pdf v0.1.1
```

The `Module` struct has a `String` method that formats this line of output, so that the default format is equivalent to `-f '{{.String}}'`.

Note that when a module has been replaced, its `Replace` field describes the replacement module, and its `Dir` field is set to the replacement module's source code, if present. (That is, if `Replace` is non-nil, then `Dir` is set to `Replace.Dir`, with no access to the replaced source code.)

The `-u` flag adds information about available upgrades. When the latest version of a given module is newer than the current one, `list -u` sets the module's `Update` field to information about the newer module. `list -u` also prints whether the currently selected version is [retracted](#glos-retracted-version) and whether the module is [deprecated](#go-mod-file-module-deprecation). The module's `String` method indicates an available upgrade by formatting the newer version in brackets after the current version. For example, `go list -m -u all` might print:

```
example.com/main/module
golang.org/x/old v1.9.9 (deprecated)
golang.org/x/net v0.1.0 (retracted) [v0.2.0]
golang.org/x/text v0.3.0 [v0.4.0] => /tmp/text
rsc.io/pdf v0.1.1 [v0.1.2]
```

(For tools, `go list -m -u -json all` may be more convenient to parse.)

The `-versions` flag causes `list` to set the module's `Versions` field to a list of all known versions of that module, ordered according to semantic versioning, lowest to highest. The flag also changes the default output format to display the module path followed by the space-separated version list. Retracted versions are omitted from this list unless the `-retracted` flag is also specified.

The `-retracted` flag instructs `list` to show retracted versions in the list printed with the `-versions` flag and to consider retracted versions when resolving [version queries](#version-queries). For example, `go list -m -retracted example.com/m@latest` shows the highest release or pre-release version of the module `example.com/m`, even if that version is retracted. [`retract` directives](#go-mod-file-retract) and [deprecations](#go-mod-file-module-deprecation) are loaded from the `go.mod` file at this version. The `-retracted` flag was added in Go 1.16.

The template function `module` takes a single string argument that must be a module path or query and returns the specified module as a `Module` struct. If an error occurs, the result will be a `Module` struct with a non-nil `Error` field.

### `go mod download`

Usage:

```
go mod download [-x] [-json] [-reuse=old.json] [modules]
```

Example:

```
$ go mod download
$ go mod download golang.org/x/mod@v0.2.0
```

The `go mod download` command downloads the named modules into the [module cache](#glos-module-cache). Arguments can be module paths or module patterns selecting dependencies of the main module or [version queries](#version-queries) of the form `path@version`. With no arguments, `download` applies to all dependencies of the [main module](#glos-main-module).

The `go` command will automatically download modules as needed during ordinary execution. The `go mod download` command is useful mainly for pre-filling the module cache or for loading data to be served by a [module proxy](#glos-module-proxy).

By default, `download` writes nothing to standard output. It prints progress messages and errors to standard error.

The `-json` flag causes `download` to print a sequence of JSON objects to standard output, describing each downloaded module (or failure), corresponding to this Go struct:

```go
type Module struct {
    Path     string // module path
    Query    string // version query corresponding to this version
    Version  string // module version
    Error    string // error loading module
    Info     string // absolute path to cached .info file
    GoMod    string // absolute path to cached .mod file
    Zip      string // absolute path to cached .zip file
    Dir      string // absolute path to cached source root directory
}
```
----
