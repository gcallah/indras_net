import React from 'react';
import {Link} from 'react-router-dom';
import handleClick from './ActionMenu';

function MenuItem(action, text) {
    return (
        <Link class="text-primary"
            onClick={() => handleClick(action)}
        >
        { text }
        </Link>
    );
}

export default MenuItem;
