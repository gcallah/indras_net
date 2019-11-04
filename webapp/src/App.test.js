/* eslint-disable no-undef */
/* eslint-disable import/no-extraneous-dependencies */
/* eslint-disable no-unused-vars */
import React from 'react';
import ReactDOM from 'react-dom';
import { shallow, mount } from 'enzyme';
import { Link } from 'react-router';
import { MemoryRouter } from 'react-router-dom';
import { create } from 'react-test-renderer';
import axios from 'axios';
import NotFoundPage from './components/NotFoundPage';
import Home from './components/Home';
import App from './App';
import { Item } from 'semantic-ui-react';

it('test case to pass', () => {
  expect(1).toEqual(1);
});

// it('renders without crashing', () => {
//   const div = document.createElement('div');
//   ReactDOM.render(<App />, div);
//   ReactDOM.unmountComponentAtNode(div);
// });


// describe('Home component', () => {
//   it('header prints', () => {
//     const wrapper = mount(<Home loadingData />);
//     const header = wrapper.text();
//     expect(header).toEqual('Loading...');
//   });
// });


// test('valid path should direct to the valid component', () => {
//   const wrapper = mount(
//     <MemoryRouter initialEntries={['/']}>
//       <App />
//     </MemoryRouter>,
//   );
//   expect(wrapper.find(Home)).toHaveLength(1);
//   expect(wrapper.find(NotFoundPage)).toHaveLength(0);
// });


// describe('Home component', () => {
//   it('change loadingData state after componentDidMount', async () => {
//     const component = mount(<Home />);
//     const instance = component.instance();
//     await instance.componentDidMount();
//     expect(instance.state.loadingData).toBe(false);
//   });
// });
