import React from 'react';
import autoBind from 'react-autobind';
import PropTypes from 'prop-types';

export default class ModelStatusBox extends React.Component {
  constructor(props) {
    super(props);
    autoBind(this);
    const { msg, title } = this.props;
    this.state = {
      msg,
      title,
    };
  }

  static getDerivedStateFromProps(nextProps, prevState) {
    if (nextProps.msg !== prevState.msg) {
      return { msg: nextProps.msg };
    }
    return null;
  }

  render() {
    const { msg, title } = this.state;
    return (
      <div>
        <div className="card w-50 model-status">
          <h5
            style={{ textAlign: 'center', fontSize: 16 }}
            className="card-header bg-primary text-white"
          >
            { title }
          </h5>
          <div className="card-body overflow-auto">
            <pre className="card-text">
              { msg }
            </pre>
          </div>
        </div>
      </div>
    );
  }
}

ModelStatusBox.propTypes = {
  msg: PropTypes.string,
  title: PropTypes.string,
};

ModelStatusBox.defaultProps = {
  msg: '',
  title: '',
};
