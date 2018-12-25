import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

const AllBooks = [
  //Tools Books
  {name:"各种包管理工具技能", link:"Tools-Books/PackagesToolsGet/book/index.html"}
]

function BooksList(props) {
  const listItems = props.books.map((oneBook) =>
    <li key>
      <a href={oneBook.link}> {oneBook.name} </a>
    </li>
  );

  return (
    <ul>{listItems}</ul>
  )
}

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <BooksList books={AllBooks}/>>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header>
      </div>
    );
  }
}

export default App;
