import React from 'react';
import { mount } from 'enzyme';
import { Link, HashRouter as Router } from 'react-router-dom';
import { Button } from 'react-bootstrap';
import CreateModelButton from '../CreateModelButton';

describe('<CreateModelButton/>', () => {
  it('<CreateModelButton /> should render <Router/>', () => {
    const component = mount(<CreateModelButton />);
    expect(component.find(Router)).toHaveLength(1);
  });

  it('<CreateModelButton /> should render <Link/> with correct props', () => {
    const component = mount(<CreateModelButton />);
    expect(component.find(Router)).toHaveLength(1);
    expect(component.find(Link)).toHaveLength(1);
    const props = component.find(Link).props();
    expect(props).toEqual({ to: 'modelcreator', children: expect.anything() });
    expect(component.find(Link)).toHaveLength(1);
  });

  it('<CreateModelButton /> should render <Button/> with correct props', () => {
    const component = mount(<CreateModelButton />);
    expect(component.find(Router)).toHaveLength(1);
    expect(component.find(Link)).toHaveLength(1);
    expect(component.find(Button)).toHaveLength(1);
    const ButtonProps = component.find(Button).props();
    expect(ButtonProps).toEqual({
      variant: 'outline-primary',
      children: 'Create a new model',
      active: false,
      disabled: false,
      type: 'button',
    });
  });
});
