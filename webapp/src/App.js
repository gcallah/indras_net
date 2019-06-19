import React, { Component } from 'react';
import { HashRouter, Route, Switch } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './components/Home';
import WIP from './components/WIP';
import ModelDetail from './components/ModelDetail'

class App extends Component {
  render() {
    return (
      <HashRouter>
        <Layout>
          <Switch>
            <Route exact path="/" component={Home} />
            <Route exact path="/wip" component={WIP} />
            <Route exact path="/models/props/:id" component={ModelDetail} />
          </Switch>
        </Layout>
      </HashRouter>
    );
  }
}

export default App;