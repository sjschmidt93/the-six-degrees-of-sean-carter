import React from 'react'
import logo from './logo.svg'
import './App.css'

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = { query: "" }
  }

  onSubmit = e => {
    e.preventDefault()
    console.log(this.state.query)
    fetch(`/search/${this.state.query}`)
      .then(res => res.json())
      .then(data => console.log(data))
  }

  onChangeQuery = e => {
    this.setState({ query: e.target.value })
    e.preventDefault()
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reloadd.
          </p>
          <form onSubmit={this.onSubmit}>
            <label>
              Search for an artist:
              <br />
              <input type="text" value={this.state.query} onChange={this.onChangeQuery} />
            </label>
            <input type="submit" value="Search" />
          </form>
        </header>
      </div>
    )
  }
}

export default App;
