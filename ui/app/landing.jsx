import React from 'react';
import ProjectsTable from './projects-table';

var Landing = React.createClass({

    getInitialState: function() {
        return {
            projects: [{id: 1, name: "poo", pee: "wumbo"}],
        }
    },

    componentDidMount: function() {
        this.projectsRequest = $.get("/api/projects", function(result) {
            this.setState({
                projects: result
            })
        }.bind(this));
    },

    componentWillUnmount: function() {
        this.projectsRequest.abort();
    },

    render: function() {
        return (
            <ProjectsTable projects={this.state.projects} />
        );
    },

});

export default Landing;
