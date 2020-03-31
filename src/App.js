import React from 'react'
import logo from './logo.svg'
import './App.css'

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = { query: "", artistOne: null, artistTwo: null }
  }

  onSelectArtistOne = artist => this.setState({artistOne: artist})

  render() {
    let text
    if (this.state.artistOne !== null) {
      text = `You have selected ${this.state.artistOne.name}. Now pick another artist.`
    } else {
      text = "Pick two artists below."
    }
    return (
      <div className="App">
        <header className="App-header">
          <p>The Six Degrees of Sean Carter</p>
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            {text}
          </p>
          <SearchForm onSelect={this.onSelectArtistOne} />
        </header>
      </div>
    )
  }
}

class SearchForm extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      query: "",
      results: []
    }
  }

  onSubmit = e => {
    e.preventDefault()
    console.log(this.state.query)
    fetch(`/search/${this.state.query}`)
      .then(res => res.json())
      .then(data => this.setState({ results: data.artists }))
  }

  onChangeQuery = e => {
    this.setState({ query: e.target.value })
    e.preventDefault()
  }

  onSelect = artist => {
    this.setState({ results: [] })
    this.props.onSelect(artist)
  }

  render() {
    return (
      <form onSubmit={this.onSubmit}>
        <label>
          Search for an artist:
          <br />
          <input type="text" value={this.state.query} onChange={this.onChangeQuery} />
        </label>
        <input type="submit" value="Search" />
        <SearchResults results={this.state.results} onSelect={this.onSelect}/>
      </form>
    )
  }
}

class SearchResults extends React.Component {
  constructor(props) {
    super(props)
  }

  render() {
    if (this.props.results === []) {
      return null
    }

    return (
      <div style={{display: 'flex', flexDirection: 'column'}}>
      {
        this.props.results.map(result => {
          return (
            <button onClick={() => this.props.onSelect(result)}>
              <h1 className="resultText">{result.name}</h1>
            </button>
          )
        })
      }
      </div>
    )
  }
}

export default App;
