import React from 'react';
import { Loader, Dimmer } from 'semantic-ui-react';

function PageDimmer() {
  return (
    <Dimmer active inverted>
      <Loader size="massive">Loading...</Loader>
    </Dimmer>
  );
}

export default PageDimmer;
