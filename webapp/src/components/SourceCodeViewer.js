import React from 'react';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { docco } from 'react-syntax-highlighter/dist/esm/styles/hljs';
import PropTypes from 'prop-types';

const SourceCodeViewer = ({ loadingData, code }) => {
  if (loadingData) {
    return (
      <SyntaxHighlighter language="python" style={docco}>
        {code}
      </SyntaxHighlighter>
    );
  }
  return null;
};

SourceCodeViewer.propTypes = {
  loadingData: PropTypes.bool,
  code: PropTypes.string,
};

SourceCodeViewer.defaultProps = {
  loadingData: true,
  code: '',
};

export default SourceCodeViewer;
