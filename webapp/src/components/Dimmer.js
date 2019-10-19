import React from "react";
import { Loader, Dimmer, DimmerDimmable } from "semantic-ui-react";

function Dimmer() {
  return (
    <Dimmer active inverted>
      <Loader size="massive">Loading...</Loader>
    </Dimmer>
  )
}

export default Dimmer;