import React from 'react';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { docco } from 'react-syntax-highlighter/dist/esm/styles/hljs';

const SourceCodeViewer = (props) => {
  const codeString = props.code;
  if (props.loadingData) {
    return (
      <SyntaxHighlighter language="javascript" style={docco}>
        {codeString}
      </SyntaxHighlighter>
    );
  } else {
    return null;
  }
};

export default SourceCodeViewer;