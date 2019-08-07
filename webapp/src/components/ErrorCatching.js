import React, { Component } from "react";
import { Loader, Dimmer } from "semantic-ui-react";

class ErrorCatching extends Component {
    state = {
    msg: '',
    loadingData: false,
    }

    async componentDidMount() {
        this.setState({ loadingData: true });
        document.title = "Indra | Work in Progress";
        this.setState({ loadingData: false });
    }

    render() {
        if (this.state.loadingData) {
            return (
                <Dimmer active inverted>
                <Loader size='massive'>Loading...</Loader>
                </Dimmer>
            );
        }

        return (
            <div>
                <br />
                <h1 style={{ "textAlign": "center" }}>Indra ABM platform
                </h1>
                <br /><br />

                <p>We are encountering some problems with the API server.
                We will have this model running soon!</p>

                <br /><br />
            </div>
        );
    }
}

export default ErrorCatching;
