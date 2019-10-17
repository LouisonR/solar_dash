#Generic graph layout
generic_layout = dict(title="",
                    autosize=False,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    type = "int",
                    xaxis=dict(rangeselector=dict(
                                                buttons=list([
                                                    dict(count=1,
                                                         label="1m",
                                                         step="month",
                                                         stepmode="backward"),
                                                    dict(count=6,
                                                         label="6m",
                                                         step="month",
                                                         stepmode="backward"),
                                                    dict(count=1,
                                                         label="YTD",
                                                         step="year",
                                                         stepmode="todate"),
                                                    dict(count=1,
                                                         label="1y",
                                                         step="year",
                                                         stepmode="backward"),
                                                    dict(step="all")
                                                ])
                                            ),
                            rangeslider=dict(visible=True),
                            )
        )

#Specific date graph layout
date_layout = dict(generic_layout)
date_layout["type"] = "date"
