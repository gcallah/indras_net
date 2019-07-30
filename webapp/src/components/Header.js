import React from 'react';
import { Menu } from 'semantic-ui-react';
import { Link } from 'react-router-dom';

export default props => {
	return (
		<div>
			<Menu.Item><Link to='/'></Link></Menu.Item>
			<Menu.Menu position="right">
			<Menu.Item><Link to='/'></Link></Menu.Item>
			</Menu.Menu>
		</div>
	);
};
