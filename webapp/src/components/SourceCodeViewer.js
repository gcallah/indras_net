import React from 'react';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { docco } from 'react-syntax-highlighter/dist/esm/styles/hljs';
import PropTypes from 'prop-types';
import CardWrapper from './CardWrapper';

const SourceCodeViewer = ({ loadingData, code }) => {
  if (loadingData) {
    return (
      <CardWrapper title="Source Code">
        <SyntaxHighlighter language="python" style={docco}>
          {code}
        </SyntaxHighlighter>
      </CardWrapper>
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
