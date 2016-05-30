import React from 'react';
import ResourceTable from './resource-table';

var ResultsTable = React.createClass({

    columnTitles: [
        "Id", "Build Id", "Project Id", "Result", "Result Message",
        "Test Name", "Timestamp",
    ],
    columnKeys: [
        "id", "build_id", "project_id", "result", "result_message",
        "test_name", "timestamp",
    ],

    render: function() {
        return (
            <ResourceTable resources={this.props.results}
                           columnTitles={this.columnTitles}
                           columnKeys={this.columnKeys} />
        );
    },

});

export default ResultsTable;
