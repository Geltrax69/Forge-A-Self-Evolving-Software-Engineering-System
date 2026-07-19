url: https://legacy.reactjs.org/redirect-to-codepen/uncontrolled-components/input-type-file
----

[Powered by](https://www.algolia.com/?utm_source=react-instantsearch\&utm_medium=website\&utm_content=codepen.io\&utm_campaign=poweredby)

##### About External Resources

You can apply CSS to your Pen from any stylesheet on the web. Just put a URL to it here and we'll apply it, in the order you have them, before the CSS in the Pen itself.

You can also link to another Pen here (use the `.css` [URL Extension](https://blog.codepen.io/documentation/url-extensions/)) and we'll pull the CSS from that Pen and include it. If it's using a *matching* preprocessor, use the appropriate URL Extension and we'll combine the code before preprocessing, so you can use the linked Pen as a true dependency.

[Learn more](https://blog.codepen.io/documentation/editor/adding-external-resources/)

[Powered by](https://www.algolia.com/?utm_source=react-instantsearch\&utm_medium=website\&utm_content=codepen.io\&utm_campaign=poweredby)

##### About External Resources

You can apply a script from anywhere on the web to your Pen. Just put a URL to it here and we'll add it, in the order you have them, before the JavaScript in the Pen itself.

If the script you link to has the file extension of a preprocessor, we'll attempt to process it before applying.

You can also link to another Pen here, and we'll pull the JavaScript from that Pen and include it. If it's using a matching preprocessor, we'll combine the code before preprocessing, so you can use the linked Pen as a true dependency.

[Learn more](https://blog.codepen.io/documentation/adding-external-resources/)

\+ add another resource

### Packages

#### Add Packages

Search for and use JavaScript packages from [npm](https://www.npmjs.com/) here. By selecting a package, an `import` statement will be added to the top of the JavaScript editor for this package.

*
*
*
*
*
*
*

```
              
                <div id="root"></div>
              
            
```

!

```
              
                
              
            
```

!

## JS

```
              
                class FileInput extends React.Component {
  constructor(props) {
    // highlight-range{3}
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.fileInput = React.createRef();
  }
  handleSubmit(event) {
    // highlight-range{3}
    event.preventDefault();
    alert(
      `Selected file - ${this.fileInput.current.files[0].name}`
    );
  }

  render() {
    // highlight-range{5}
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          Upload file:
          <input type="file" ref={this.fileInput} />
        </label>
        <br />
        <button type="submit">Submit</button>
      </form>
    );
  }
}

const root = ReactDOM.createRoot(
  document.getElementById('root')
);
root.render(<FileInput />);

              
            
```

!

999px

If you get tired, be like an AJAX request and REST.

----
