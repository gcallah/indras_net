import React from 'react';

function PreFormTextBox(title, text) {
    return (
    <div>
        <h5 style={{textAlign: 'center', "fontSize": 16}}
            className="card-header bg-primary text-white">{ title }</h5>
        <div className="card-body">
        <p class="card-text">
        {text}
        </p>
        </div>
    </div>);
}

export default PreFormTextBox;
