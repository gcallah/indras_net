import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { shallow , mount} from 'enzyme';
import Home from './components/Home';


it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<App />, div);
  ReactDOM.unmountComponentAtNode(div); 

});
 

describe('Home component', () => {
      it('header prints', () => {
        const wrapper = mount(<Home loadingData={true}/>);
        const header = wrapper.text();
        expect(header).toEqual('Loading...');
      });
    });




