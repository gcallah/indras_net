import React from 'react';
import { mount } from 'enzyme';
import Menu from '../Menu';

describe('<Menu/>', () => {
  it('<Menu /> should render <ul/> with correct props', () => {
    const component = mount(<Menu />);
    expect(component.find('ul')).toHaveLength(1);
    expect(component.find('ul').props()).toEqual({
      children: expect.anything(),
      className: 'list-group',
    });
  });

  it('<Menu /> should render two <div />', () => {
    const component = mount(<Menu />);
    expect(component.find('ul')).toHaveLength(1);
    expect(component.find('div')).toHaveLength(2);
  });
});
