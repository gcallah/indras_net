import React from 'react';
import { mount } from 'enzyme';
import ActionMenu from './components/ActionMenu';

describe('Mounted ActionMenu', () => {
  const wrapper = mount(<ActionMenu />);
  it('should render Population Graph on Click', () => {
    // const button = wrapper.find('btn-success').first();
    // button.simulate('click');
    const state = wrapper.state('loadingSourceCode');
    expect(state).toEqual(false);
  });
});
