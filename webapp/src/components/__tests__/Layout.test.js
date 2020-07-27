import React from 'react';
import { mount } from 'enzyme';
import { Container } from 'semantic-ui-react';
import { HashRouter } from 'react-router-dom';
import Layout from '../Layout';
import Header from '../Header';

describe('<Layout/>', () => {
  it('<Layout /> should render <Container/>', () => {
    const children = <div className="foo">foo</div>;
    const component = mount(<HashRouter><Layout>{children}</Layout></HashRouter>);
    expect(component.find(Container)).toHaveLength(1);
  });

  it('<Layout /> should render <link/> with correct props', () => {
    const children = <div className="foo">foo</div>;
    const component = mount(<HashRouter><Layout>{children}</Layout></HashRouter>);
    expect(component.find(Container)).toHaveLength(1);
    expect(component.find('link')).toHaveLength(1);
    const props = component.find('link').props();
    expect(props).toEqual({
      href:
        '//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css',
      rel: 'stylesheet',
    });
  });

  it('<Layout /> should render <Header/>', () => {
    const children = <div className="foo">foo</div>;
    const component = mount(<HashRouter><Layout>{children}</Layout></HashRouter>);
    expect(component.find(Container)).toHaveLength(1);
    expect(component.find(Header)).toHaveLength(1);
  });

  it('<Layout /> should render children', () => {
    const children = <div className="foo">foo</div>;
    const component = mount(<HashRouter><Layout>{children}</Layout></HashRouter>);
    expect(component.find(Container)).toHaveLength(1);
    expect(component.find(Header)).toHaveLength(1);
    const foo = component.find('.foo');
    expect(foo.props()).toEqual({ className: 'foo', children: 'foo' });
  });
});
