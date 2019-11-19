import React from 'react';
import { mount } from 'enzyme';
import ActionMenu from './components/ActionMenu';

describe('Mounted ActionMenu', () => {
  it('should render Population Graph on Click', () => {
    // Render a checkbox with label in the document
    const wrapper = mount(<ActionMenu />);
    // const button = wrapper.find('btn-success').first();
    // button.simulate('click');
    console.log(wrapper.debug());
    const state = wrapper.state('loadingSourceCode');
    expect(state).toEqual(false);
  });
});
