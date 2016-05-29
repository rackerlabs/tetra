import React from 'react';
import ResourceTable from './resource-table';

var ResultsTable = React.createClass({

    columnKeys: [
        "id", "build_id", "project_id", "result", "result_message",
        "test_name", "timestamp",
    ],

    render: function() {
        return (
            <ResourceTable resources={this.props.results}
                           columnKeys={this.columnKeys} />
        );
    },

});

export default ResultsTable;
