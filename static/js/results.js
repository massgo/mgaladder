var ResultsBox = React.createClass({
    getInitialState: function() {
        return {data:{results:[]}};
    },
    // Does not update automatically yet
    componentDidMount: function() {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            success: function(data) {
                this.setState({data:data});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    render: function(){
        return (
            <div className="resultsBox">
                <h2>Results</h2>
                <ResultsList data={this.state.data} />
            </div>
        );
    }
});

var ResultsList = React.createClass({
    render: function() {
        var resultNodes = this.props.data.results.map(function (result) {
            return (
                <li>black = {result.black}, white = {result.white}</li>
            );
        });
        
        return (
            <div className="resultsList">
                <h3>Results should be here</h3>
                <ol>
                {resultNodes}
                </ol>
            </div>
        );
    }
});

//Render All
data = {'results': [
    {'black':'Walther', 'white':'Andrew'},
    {'black':'Walther', 'white':'Chun'}
    ]};
React.render(
    <ResultsBox url="http://localhost:5000/results" />,
    document.getElementById('results')
);
