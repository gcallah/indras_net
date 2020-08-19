/* eslint-disable no-undef */
/* eslint-disable import/no-extraneous-dependencies */
/* eslint-disable no-unused-vars */

import React from 'react';
import { mount } from 'enzyme';
import { ThemeProvider } from 'styled-components';
import { MemoryRouter, HashRouter, Switch } from 'react-router-dom';
import App, { IndraRoutes } from './App';
import Layout from './components/Layout';
import Home from './components/Home';
import WIP from './components/WIP';
import ModelDetail from './components/ModelDetail';
import ActionMenu from './components/ActionMenu';
import NotFoundPage from './components/NotFoundPage';
import ErrorCatching from './components/ErrorCatching';

const CLI_EXEC_KEY = 0;

describe('<App/>', () => {
  it('renders with <HashRouter/>, <Layout/> and <Swtich/>', () => {
    const defaultTheme = {};
    const component = mount(
      <ThemeProvider theme={defaultTheme}>
        <App />
      </ThemeProvider>,
    );
    expect(component.find(HashRouter)).toHaveLength(1);
    expect(component.find(Layout)).toHaveLength(1);
    expect(component.find(Switch)).toHaveLength(1);
  });

  describe('renders valid component when a route is called', () => {
    it('home route renders <Home/> component', () => {
      const component = mount(
        <MemoryRouter initialEntries={['/']}>
          <IndraRoutes />
        </MemoryRouter>,
      );
      expect(component.find(Home)).toHaveLength(1);
      expect(component.find(NotFoundPage)).toHaveLength(0);
      expect(component.find(WIP)).toHaveLength(0);
      expect(component.find(ModelDetail)).toHaveLength(0);
      expect(component.find(ErrorCatching)).toHaveLength(0);
      expect(component.find(ActionMenu)).toHaveLength(0);
    });

    it('WIP route renders <WIP/> component', () => {
      const component = mount(
        <MemoryRouter initialEntries={['/wip']}>
          <IndraRoutes />
        </MemoryRouter>,
      );
      expect(component.find(Home)).toHaveLength(0);
      expect(component.find(NotFoundPage)).toHaveLength(0);
      expect(component.find(WIP)).toHaveLength(1);
      expect(component.find(ModelDetail)).toHaveLength(0);
      expect(component.find(ErrorCatching)).toHaveLength(0);
      expect(component.find(ActionMenu)).toHaveLength(0);
    });

    it('ModelDetail route renders <ModelDetail/> component', () => {
      const component = mount(
        <MemoryRouter initialEntries={[{
          pathname: '/models/props/2',
          state: {
            menuId: 2, name: 'test_name', source: 'test_source', graph: 'test_graph', envFile: { execution_key: CLI_EXEC_KEY },
          },
        }]}
        >
          <IndraRoutes />
        </MemoryRouter>,
      );
      expect(component.find(Home)).toHaveLength(0);
      expect(component.find(NotFoundPage)).toHaveLength(0);
      expect(component.find(WIP)).toHaveLength(0);
      expect(component.find(ModelDetail)).toHaveLength(1);
      expect(component.find(ErrorCatching)).toHaveLength(0);
      expect(component.find(ActionMenu)).toHaveLength(0);
    });

    it('ActionMenu route renders <ActionMenu/> component', () => {
      const component = mount(
        <MemoryRouter initialEntries={[{ pathname: `/models/menu/${CLI_EXEC_KEY}`, state: { envFile: { execution_key: CLI_EXEC_KEY } } }]}>
          <IndraRoutes />
        </MemoryRouter>,
      );
      expect(component.find(Home)).toHaveLength(0);
      expect(component.find(NotFoundPage)).toHaveLength(0);
      expect(component.find(WIP)).toHaveLength(0);
      expect(component.find(ModelDetail)).toHaveLength(0);
      expect(component.find(ErrorCatching)).toHaveLength(0);
      expect(component.find(ActionMenu)).toHaveLength(1);
    });

    it('ErrorCatching route renders <ErrorCatching/> component', () => {
      const component = mount(
        <MemoryRouter initialEntries={['/errorCatching']}>
          <IndraRoutes />
        </MemoryRouter>,
      );
      expect(component.find(Home)).toHaveLength(0);
      expect(component.find(NotFoundPage)).toHaveLength(0);
      expect(component.find(WIP)).toHaveLength(0);
      expect(component.find(ModelDetail)).toHaveLength(0);
      expect(component.find(ErrorCatching)).toHaveLength(1);
      expect(component.find(ActionMenu)).toHaveLength(0);
    });
    it('NotFoundPage route renders <NotFoundPage/> component', () => {
      const component = mount(
        <MemoryRouter initialEntries={['/random']}>
          <IndraRoutes />
        </MemoryRouter>,
      );
      expect(component.find(Home)).toHaveLength(0);
      expect(component.find(NotFoundPage)).toHaveLength(1);
      expect(component.find(WIP)).toHaveLength(0);
      expect(component.find(ModelDetail)).toHaveLength(0);
      expect(component.find(ErrorCatching)).toHaveLength(0);
      expect(component.find(ActionMenu)).toHaveLength(0);
    });
  });
});
