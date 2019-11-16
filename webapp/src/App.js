import React from 'react';
import { HashRouter, Route, Switch } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './components/Home';
import WIP from './components/WIP';
import ModelDetail from './components/ModelDetail';
import ActionMenu from './components/ActionMenu';
import NotFoundPage from './components/NotFoundPage';
import ErrorCatching from './components/ErrorCatching';

function App() {
  return (
    <HashRouter>
      <Layout>
        <Switch>
          <Route exact path="/" component={Home} />
          <Route exact path="/wip" component={WIP} />
          <Route exact path="/models/props/:id" component={ModelDetail} />
          <Route exact path="/models/menu/:id" component={ActionMenu} />
          <Route exact path="/errorCatching" component={ErrorCatching} />
          <Route component={NotFoundPage} />
        </Switch>
      </Layout>
    </HashRouter>
  );
}

export default App;
