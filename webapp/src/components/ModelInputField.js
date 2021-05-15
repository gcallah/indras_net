import React from 'react';
import PropTypes from 'prop-types';

function ModelInputField(props) {
  const {
    label, name, type, placeholder, propChange, error,
  } = props;
  return (
    <div key={label} className="form-group">
      <div>
        <label
          htmlFor={name}
          className="col-sm-4 col-md-4 col-lg-4"
          key={label}
        >
          {label}
          {' '}
          {' '}
        </label>
        <input
          // eslint-disable-next-line jsx-a11y/no-autofocus
          autoFocus
          id={name}
          type={type}
          className="col-sm-2 col-md-2 col-lg-2"
          style={{ fontSize: '15pt' }}
          placeholder={placeholder}
          onChange={propChange} /* style={{width: 60}} */
          name={name}
        />
        <span className="col-sm-6 col-md-6 col-lg-6" style={{ color: 'red', fontSize: 12 }}>
          {error}
        </span>
        <br />
      </div>
    </div>
  );
}

ModelInputField.propTypes = {
  label: PropTypes.string,
  name: PropTypes.string,
  type: PropTypes.string,
  placeholder: PropTypes.number,
  propChange: PropTypes.func,
  error: PropTypes.string,
};

ModelInputField.defaultProps = {
  label: '',
  name: '',
  type: '',
  placeholder: 0,
  propChange() {},
  error: '',
};

export default ModelInputField;
