/* eslint-disable react/prefer-stateless-function */
/* eslint-disable arrow-parens */
import React from 'react';
import { HashRouter, Route, Switch } from 'react-router-dom';
import styled, { withTheme } from 'styled-components';
import { Switch as Switch2 } from '@material-ui/core';
import Layout from './components/Layout';
import Home from './components/Home';
import WIP from './components/WIP';
import ModelDetail from './components/ModelDetail';
import ActionMenu from './components/ActionMenu';
import NotFoundPage from './components/NotFoundPage';
import ErrorCatching from './components/ErrorCatching';
import { useTheme } from './darkTheme/ThemeContext';

const Wrapper = styled('div')`
  background: ${props => props.theme.background};
  width: 100vw;
  height: 100vh;
  font-family: -apple-stem, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen";
  h1 {
    color: ${props => props.theme.body};
  }
`;

function App() {
  const themeState = useTheme();
  return (
    <Wrapper>
      <div>
        <Switch2
          defaultChecked
          value="checkedF"
          color="default"
          inputProps={{ 'aria-label': 'checkbox with default color' }}
          onClick={() => themeState.toggle()}
        />
      </div>
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
    </Wrapper>
  );
}

export default withTheme(App);
