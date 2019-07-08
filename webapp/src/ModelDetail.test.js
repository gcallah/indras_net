import React from 'react';
import { shallow , mount} from 'enzyme';
import ModelDetail from './components/ModelDetail';
import { create } from "react-test-renderer";
import axios from 'axios';
import ReactDOM from 'react-dom';

describe("ModelDetail component", () => {
  it("has Submit button",() => {
    const component = mount(<ModelDetail {...props}/>);
    expect(component.find('h2').text()).toEqual('Please set the parameters for your model')
  });
});


describe("ModelDetail component", () => {
  it("change loadingData state after componentDidMount", async () => {
    const component = mount(<ModelDetail />);
    const instance = component.instance();
    await instance.componentDidMount();
    expect(instance.state.loadingData).toBe(false)
  });
});