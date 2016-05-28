import React from 'react';
import ResourceTable from './resource-table';

var BuildsTable = React.createClass({

    columnKeys: ["Id", "Name", "Build_url", "Region", "Environment"],

    render: function() {
        return (
            <ResourceTable resources={this.props.builds}
                           columnKeys={this.columnKeys} />
        );
    },

});

export default BuildsTable;
