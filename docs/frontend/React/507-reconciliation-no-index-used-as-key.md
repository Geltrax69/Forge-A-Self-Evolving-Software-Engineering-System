url: https://legacy.reactjs.org/redirect-to-codepen/reconciliation/no-index-used-as-key
----

```
```

[Powered by](https://www.algolia.com/?utm_source=react-instantsearch\&utm_medium=website\&utm_content=codepen.io\&utm_campaign=poweredby)

##### About External Resources

You can apply CSS to your Pen from any stylesheet on the web. Just put a URL to it here and we'll apply it, in the order you have them, before the CSS in the Pen itself.

You can also link to another Pen here (use the `.css` [URL Extension](https://blog.codepen.io/documentation/url-extensions/)) and we'll pull the CSS from that Pen and include it. If it's using a *matching* preprocessor, use the appropriate URL Extension and we'll combine the code before preprocessing, so you can use the linked Pen as a true dependency.

[Learn more](https://blog.codepen.io/documentation/editor/adding-external-resources/)

?

##### Insecure Resource

You are linking to a resource using the non-secure http\:// protocol, which may not work when the browser is using https\:// like CodePen enforces.

?

##### URL Extension Required

When linking another Pen as a resource, make sure you use a [URL Extension](https://blog.codepen.io/documentation/url-extensions/) of the type of code you want to link to. Either `.css`, `.js`, or the extension of a matching code processor.

[]()

?

##### Insecure Resource

You are linking to a resource using the non-secure http\:// protocol, which may not work when the browser is using https\:// like CodePen enforces.

?

##### URL Extension Required

When linking another Pen as a resource, make sure you use a [URL Extension](https://blog.codepen.io/documentation/url-extensions/) of the type of code you want to link to. Either `.css`, `.js`, or the extension of a matching code processor.

[]()

```
```

[Powered by](https://www.algolia.com/?utm_source=react-instantsearch\&utm_medium=website\&utm_content=codepen.io\&utm_campaign=poweredby)

##### About External Resources

You can apply a script from anywhere on the web to your Pen. Just put a URL to it here and we'll add it, in the order you have them, before the JavaScript in the Pen itself.

If the script you link to has the file extension of a preprocessor, we'll attempt to process it before applying.

You can also link to another Pen here, and we'll pull the JavaScript from that Pen and include it. If it's using a matching preprocessor, we'll combine the code before preprocessing, so you can use the linked Pen as a true dependency.

[Learn more](https://blog.codepen.io/documentation/adding-external-resources/)

?

##### Insecure Resource

You are linking to a resource using the non-secure http\:// protocol, which may not work when the browser is using https\:// like CodePen enforces.

?

##### URL Extension Required

When linking another Pen as a resource, make sure you use a [URL Extension](https://blog.codepen.io/documentation/url-extensions/) of the type of code you want to link to. Either `.css`, `.js`, or the extension of a matching code processor.

[](//unpkg.com/react/umd/react.development.js)

?

##### Insecure Resource

You are linking to a resource using the non-secure http\:// protocol, which may not work when the browser is using https\:// like CodePen enforces.

?

##### URL Extension Required

When linking another Pen as a resource, make sure you use a [URL Extension](https://blog.codepen.io/documentation/url-extensions/) of the type of code you want to link to. Either `.css`, `.js`, or the extension of a matching code processor.

[](//unpkg.com/react-dom/umd/react-dom.development.js)

\+ add another resource

### Packages

#### Add Packages

Search for and use JavaScript packages from [npm](https://www.npmjs.com/) here. By selecting a package, an `import` statement will be added to the top of the JavaScript editor for this package.

```
```

## HTML

 

1

```
<div id="root"></div>
```

!

## CSS

​x

 

1

```
​
```

!

## JS (Babel)

## JS (Babel)

```
xxxxxxxxxx
```

111

 

1

```
const ToDo = props => (
```

2

```
  <tr>
```

3

```
    <td>
```

4

```
      <label>{props.id}</label>
```

5

```
    </td>
```

6

```
    <td>
```

7

```
      <input />
```

8

```
    </td>
```

9

```
    <td>
```

10

```
      <label>{props.createdAt.toTimeString()}</label>
```

11

```
    </td>
```

12

```
  </tr>
```

13

```
);
```

14

```
​
```

15

```
class ToDoList extends React.Component {
```

16

```
  constructor() {
```

17

```
    super();
```

18

```
    const date = new Date();
```

19

```
    const toDoCounter = 1;
```

20

```
    this.state = {
```

21

```
      list: [
```

22

```
        {
```

23

```
          id: toDoCounter,
```

24

```
          createdAt: date,
```

25

```
        },
```

26

```
      ],
```

27

```
      toDoCounter: toDoCounter,
```

28

```
    };
```

29

```
  }
```

30

```
​
```

31

```
  sortByEarliest() {
```

32

```
    const sortedList = this.state.list.sort((a, b) => {
```

33

```
      return a.createdAt - b.createdAt;
```

34

```
    });
```

35

```
    this.setState({
```

36

```
      list: [...sortedList],
```

37

```
    });
```

38

```
  }
```

39

```
​
```

40

```
  sortByLatest() {
```

41

```
    const sortedList = this.state.list.sort((a, b) => {
```

42

```
      return b.createdAt - a.createdAt;
```

43

```
    });
```

44

```
    this.setState({
```

45

```
      list: [...sortedList],
```

46

```
    });
```

47

```
  }
```

48

```
​
```

49

```
  addToEnd() {
```

50

```
    const date = new Date();
```

51

```
    const nextId = this.state.toDoCounter + 1;
```

52

```
    const newList = [
```

53

```
      ...this.state.list,
```

54

```
      {id: nextId, createdAt: date},
```

55

```
    ];
```

56

```
    this.setState({
```

57

```
      list: newList,
```

58

```
      toDoCounter: nextId,
```

59

```
    });
```

60

```
  }
```

61

```
​
```

62

```
  addToStart() {
```

63

```
    const date = new Date();
```

64

```
    const nextId = this.state.toDoCounter + 1;
```

65

```
    const newList = [
```

66

```
      {id: nextId, createdAt: date},
```

67

```
      ...this.state.list,
```

68

```
    ];
```

69

```
    this.setState({
```

70

```
      list: newList,
```

71

```
      toDoCounter: nextId,
```

72

```
    });
```

73

```
  }
```

74

```
​
```

75

```
  render() {
```

76

```
    return (
```

77

```
      <div>
```

78

```
        <code>key=id</code>
```

79

```
        <br />
```

80

```
        <button onClick={this.addToStart.bind(this)}>
```

81

```
          Add New to Start
```

82

```
        </button>
```

83

```
        <button onClick={this.addToEnd.bind(this)}>
```

84

```
          Add New to End
```

85

```
        </button>
```

86

```
        <button onClick={this.sortByEarliest.bind(this)}>
```

87

```
          Sort by Earliest
```

88

```
        </button>
```

89

```
        <button onClick={this.sortByLatest.bind(this)}>
```

90

```
          Sort by Latest
```

91

```
        </button>
```

92

```
        <table>
```

93

```
          <tr>
```

94

```
            <th>ID</th>
```

95

```
            <th />
```

96

```
            <th>created at</th>
```

97

```
          </tr>
```

98

```
          {this.state.list.map((todo, index) => (
```

99

```
            <ToDo key={todo.id} {...todo} />
```

100

```
          ))}
```

101

```
        </table>
```

102

```
      </div>
```

103

```
    );
```

104

```
  }
```

105

```
}
```

106

```
​
```

107

```
ReactDOM.render(
```

108

```
  <ToDoList />,
```

109

```
  document.getElementById('root')
```

110

```
);
```

111

```
​
```

!

999px

If a groundhog inspects their Web Component, do they see their Shadow DOM?

----
