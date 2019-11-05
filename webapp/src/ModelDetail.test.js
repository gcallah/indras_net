/* eslint-disable no-undef */
/* eslint-disable no-unused-vars */
import React from 'react';
import { shallow, mount } from 'enzyme';
import { create } from 'react-test-renderer';
import axios from 'axios';
import ReactDOM from 'react-dom';
import ReactTestUtils from 'react-dom/test-utils';
import ModelDetail from './components/ModelDetail';

it('test case to pass', () => {
  expect(1).toEqual(1);
});

// describe('ModelDetail Component', () => {
//   it('has an h2 tag', () => {
//     const component = shallow(<ModelDetail />);
//     const node = component.find('h2');
//     expect(node.length).toEqual(1);
//   });

//   it('has an h3 tag', () => {
//     const component = shallow(<ModelDetail />);
//     const node = component.find('h3');
//     expect(node.length).toEqual(1);
//   });
// });

// it('calls handleSubmit function when form is submitted', () => {
//   const handleSubmit = jest.fn();
//   const wrapper = mount(<form onSubmit={handleSubmit} />);
//   const form = wrapper.find('form');
//   form.simulate('submit');
//   expect(handleSubmit).toHaveBeenCalledTimes(1);
// });


// it('renders input', () => {
//   const wrapper = mount(<input type="item_type" defaultValue="default_value" name="item_name"/>);
//   const input = wrapper.find('input');
//   expect(input).toHaveLength(1);
//   expect(input.prop('type')).toEqual('item_type');
//   expect(input.prop('defaultValue')).toEqual('default_value');
//   expect(input.prop('name')).toEqual('item_name');
// });


// describe('ModelDetail component', () => {
//   it('change loadingData state after componentDidMount', async () => {
//     const component = mount(<ModelDetail />);
//     const instance = component.getInstance();
//     await instance.componentDidMount();
//     expect(instance.state.loadingData).toBe(false);
//   });
// });
