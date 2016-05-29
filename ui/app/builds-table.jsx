import React from 'react';
import ResourceTable from './resource-table';

var BuildsTable = React.createClass({

    columnKeys: [
        "Id", "Project_id", "Name", "Build_url", "Region", "Environment"
    ],

    render: function() {
        return (
            <ResourceTable resources={this.props.builds}
                           columnKeys={this.columnKeys}
                           getRoute={this.getRoute} />
        );
    },

    getRoute: function(build) {
        return "/" + build.project_id + "/builds/" + build.id + "/results";
    },

});

export default BuildsTable;
