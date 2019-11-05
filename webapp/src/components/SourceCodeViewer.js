/* eslint-disable react/prop-types */
/* eslint-disable react/destructuring-assignment */
import React from 'react';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { docco } from 'react-syntax-highlighter/dist/esm/styles/hljs';

const SourceCodeViewer = (props) => {
  if (props.loadingData) {
    return (
      <SyntaxHighlighter language="python" style={docco}>
        {props.code}
      </SyntaxHighlighter>
    );
  }
  return null;
};

export default SourceCodeViewer;
