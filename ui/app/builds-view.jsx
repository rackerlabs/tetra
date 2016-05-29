import React from 'react';
import BuildsTable from './builds-table';

var BuildsView = React.createClass({

    getInitialState: function() {
        return {
            builds: [],
        }
    },

    projectId: function() {
        return this.props.params.project_id || this.props.project_id;
    },

    componentDidMount: function() {
        var url = "/api/" + this.projectId() + "/builds";
        this.buildsRequest = $.get(url, function(result) {
            this.setState({
                builds: result
            })
        }.bind(this))
    },

    componentWillUnmount: function() {
        this.buildsRequest.abort();
    },

    render: function() {
        return (
            <div>
                <h2 className="rs-page-title">Builds</h2>
                <BuildsTable builds={this.state.builds} />
            </div>
        );
    },
});

export default BuildsView;
