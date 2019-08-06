import React, {Component} from 'react';

const renderPreFormTextBox = (title, dispText) => {
    <div>
    <h5 style={{textAlign: 'center', "fontSize": 16}}
        class="card-header bg-primary text-white">{title}</h5>
    <div class="card-body">
    <pre>
    {dispText}
    </pre>
    </div>
    </div>
}

