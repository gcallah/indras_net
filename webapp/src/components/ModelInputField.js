import React from 'react';

function ModelInputField(props) {
  return (
    <div key={props.label} className="form-group">
      <div>
        <label
          className="col-sm-4 col-md-4 col-lg-4"
          key={props.label}
        >
          {props.label}
          {' '}
          {' '}
        </label>
        <input
          type={props.type}
          className="col-sm-2 col-md-2 col-lg-2"
          style={{ fontSize: '15pt' }}
          placeholder={props.placeholder}
          onChange={props.propChange} /* style={{width: 60}} */
          name={props.name}
        />
        <span className="col-sm-6 col-md-6 col-lg-6" style={{ color: 'red', fontSize: 12 }}>
          {props.error}
        </span>
        <br />
      </div>
    </div>
  );
}

export default ModelInputField;
