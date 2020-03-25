import React from 'react';
import { mount } from 'enzyme';
import { Link, HashRouter as Router } from 'react-router-dom';
import { Button } from 'react-bootstrap';
import BackHomeButton from '../BackHomeButton';

describe('<BackHomeButton/>', () => {
  it('<BackHomeButton /> should render <Router/>', () => {
    const component = mount(<BackHomeButton />);
    expect(component.find(Router)).toHaveLength(1);
  });

  it('<BackHomeButton /> should render <Link/> with correct props', () => {
    const component = mount(<BackHomeButton />);
    expect(component.find(Router)).toHaveLength(1);
    expect(component.find(Link)).toHaveLength(1);
    const props = component.find(Link).props();
    expect(props).toEqual({ to: '/', children: expect.anything() });
    expect(component.find(Link)).toHaveLength(1);
  });

  it('<BackHomeButton /> should render <Button/> with correct props', () => {
    const component = mount(<BackHomeButton />);
    expect(component.find(Router)).toHaveLength(1);
    expect(component.find(Link)).toHaveLength(1);
    expect(component.find(Button)).toHaveLength(1);
    const ButtonProps = component.find(Button).props();
    expect(ButtonProps).toEqual({
      variant: 'primary',
      children: 'Back Home',
      active: false,
      disabled: false,
      type: 'button',
    });
  });
});
