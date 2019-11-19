import React from 'react';
import { mount } from 'enzyme';
import ActionMenu from './components/ActionMenu';

describe('Mounted ActionMenu', () => {
  const wrapper = mount(<ActionMenu />);
  it('should render Population Graph on Click', () => {
    // const button = wrapper.find('btn-success').first();
    // button.simulate('click');
    console.log(wrapper.debug());
    const state = wrapper.state('loadingSourceCode');
    expect(state).toEqual(false);
  });
  it('should return home on home button click', () => {
    global.window = { location: { pathname: null } };
    const button = wrapper.find('BackHomeButton').first();
    button.simulate('click');
    expect(global.window.location.pathname).toEqual('/');
  });
});
