import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as shapes


from modules.DataStreamer import DataStreamer

def set_plot_area(axes, field_color='#FFFFFF', outline_color='#cccccc', xmin=-60, xmax=60, ymin=-40, ymax=40):
    '''
    This function sets the boundaries of the plotted area for the given
    axes and sets the labels of the x and y axis. Default is -60 < x < 60
    and -40 < y < 40, which covers the entire football field.
    In addition to that it plots the outline of the football field, including
    all the circles and lines marking key areas of the field.
    :param axes: The matplotlib pyplot axes to draw on
    :param field_color: Background color of the field plot
    :param outline_color: Color of the field outline
    :param xmin: The lower limit on the x axis
    :param xmax: The upper limit on the x axis
    :param ymin: The lower limit on the y axis
    :param ymax: The upper limit on the y axis
    '''

    axes.set_facecolor(field_color)
    outline_width = 1

    field_width = 68.0  # 74 yards
    field_length = 105.0  # 115 yards

    center_circle_radius = 9.144  # 10 yards
    penalty_area_width = 40.2336  # 44 yards
    penalty_area_length = 16.4592  # 18 yards
    penalty_spot_pos = 10.9728  # 12 yards
    penalty_arc_radius = 9.144  # 10 yards
    goal_area_width = 18.288  # 20 yards
    goal_area_length = 5.4864  # 6 yards
    goal_width = 7.3152  # 8 yards
    corner_arc_radius = 0.9144  # 1 yard
    corner_buffer = 9.144  # 10 yards

    # Check if the values make sense
    if xmin >= xmax:
        raise ValueError('X-axis: lower limit is greater than ',
                         'upper limit (%s > %s) ' % (xmin, xmax))

    if ymin >= ymax:
        raise ValueError('Y-axis: lower limit is greater than ',
                         'upper limit (%s > %s) ' % (ymin, ymax))

    # Plot the corners of the field
    lim_x = field_length / 2
    lim_y = field_width / 2
    field = shapes.Rectangle((-1*lim_x, -1*lim_y), field_length, field_width,
                             edgecolor=outline_color, facecolor='none')
    axes.add_patch(field)

    # Plot the penalty areas
    penalty_lim_y = penalty_area_width / 2

    # Plot the left penalty area
    left_penalty_area = shapes.Rectangle(
        (-1*lim_x, -1*penalty_lim_y), penalty_area_length, penalty_area_width,
        edgecolor=outline_color, facecolor='none')
    axes.add_patch(left_penalty_area)
    # Plot the right penalty area
    right_penalty_area = shapes.Rectangle(
        (lim_x-penalty_area_length, -1*penalty_lim_y), penalty_area_length,
        penalty_area_width, edgecolor=outline_color, facecolor='none')
    axes.add_patch(right_penalty_area)

    # Plot the penalty spots
    penalty_spot_x = lim_x - penalty_spot_pos

    # Plot the left penalty spot
    axes.plot(-1*penalty_spot_x, 0, 'o', color=outline_color,
              markersize=2*outline_width, zorder=0)
    # Plot the right penalty spot
    axes.plot(penalty_spot_x, 0, 'o', color=outline_color,
              markersize=2*outline_width, zorder=0)

    # Plot the penalty arc
    penalty_arc_corner = math.degrees(math.acos(
        (penalty_area_length-penalty_spot_pos) / penalty_arc_radius))
    # Plot the left penalty arc
    left_penalty_arc = shapes.Arc(
        (-1*penalty_spot_x, 0), width=2*penalty_arc_radius,
        height=2*penalty_arc_radius, theta1=360-penalty_arc_corner,
        theta2=penalty_arc_corner, edgecolor=outline_color, facecolor='none')
    axes.add_patch(left_penalty_arc)
    # Plot the right penalty arc
    right_penalty_arc = shapes.Arc(
        (penalty_spot_x, 0), width=2*penalty_arc_radius,
        height=2*penalty_arc_radius, theta1=180-penalty_arc_corner,
        theta2=180+penalty_arc_corner, edgecolor=outline_color,
        facecolor='none')
    axes.add_patch(right_penalty_arc)

    # Plot the goal area
    goal_area_lim_y = goal_area_width / 2

    # Plot the left goal area
    left_goal_area = shapes.Rectangle(
        (-1*lim_x, -1*goal_area_lim_y), goal_area_length, goal_area_width,
        edgecolor=outline_color, facecolor='none')
    axes.add_patch(left_goal_area)
    # Plot the right goal area
    right_goal_area = shapes.Rectangle(
        (lim_x-goal_area_length, -1*goal_area_lim_y), goal_area_length,
        goal_area_width, edgecolor=outline_color, facecolor='none')
    axes.add_patch(right_goal_area)

    # Plot the goal
    goal_lim_y = goal_width / 2
    goal_depth = 2

    # Plot the left goal
    left_goal = shapes.Rectangle(
        (-1*lim_x-goal_depth, -1*goal_lim_y), goal_depth, goal_width,
        edgecolor=outline_color, facecolor='none')
    axes.add_patch(left_goal)
    # Plot the right goal
    right_goal = shapes.Rectangle(
        (lim_x, -1*goal_lim_y), goal_depth, goal_width,
        edgecolor=outline_color, facecolor='none')
    axes.add_patch(right_goal)

    # Plot the center line
    axes.plot([0, 0], [lim_y, -1*lim_y], color=outline_color,
              linewidth=outline_width, zorder=0)

    # Plot the center circle
    center_circle = shapes.Circle(
        (0, 0), radius=center_circle_radius, edgecolor=outline_color,
        facecolor='none')
    axes.add_patch(center_circle)

    # Plot the center spot
    axes.plot(0, 0, 'o', color=outline_color,
              markersize=2*outline_width, zorder=0)

    # Plot the corner arcs

    # Plot the left corner arcs
    top_left_corner_arc = shapes.Arc(
        (-1*lim_x, lim_y), width=2*corner_arc_radius,
        height=2*corner_arc_radius, theta1=270, theta2=0,
        edgecolor=outline_color, facecolor='none')
    bottom_left_corner_arc = shapes.Arc(
        (-1*lim_x, -1*lim_y), width=2*corner_arc_radius,
        height=2*corner_arc_radius, theta1=0, theta2=90,
        edgecolor=outline_color, facecolor='none')
    axes.add_patch(top_left_corner_arc)
    axes.add_patch(bottom_left_corner_arc)
    # Plot the left corner arcs
    top_right_corner_arc = shapes.Arc(
        (lim_x, lim_y), width=2*corner_arc_radius, height=2*corner_arc_radius,
        theta1=180, theta2=270, edgecolor=outline_color, facecolor='none')
    bottom_right_corner_arc = shapes.Arc(
        (lim_x, -1*lim_y), width=2*corner_arc_radius,
        height=2*corner_arc_radius, theta1=90, theta2=180,
        edgecolor=outline_color, facecolor='none')
    axes.add_patch(top_right_corner_arc)
    axes.add_patch(bottom_right_corner_arc)

    # Plot the corner distance markers
    corner_marker_depth = 0.5
    corner_buffer_x = lim_x - corner_buffer
    corner_buffer_y = lim_y - corner_buffer

    # Add the top left corner distance markers
    axes.plot([-1*corner_buffer_x, -1*corner_buffer_x],
              [lim_y, lim_y+corner_marker_depth], color=outline_color,
              linewidth=outline_width, zorder=0)
    axes.plot([-1*lim_x, -1*lim_x-corner_marker_depth],
              [corner_buffer_y, corner_buffer_y], color=outline_color,
              linewidth=outline_width, zorder=0)
    # Add the bottom left corner distance markers
    axes.plot([-1*corner_buffer_x, -1*corner_buffer_x],
              [-1*lim_y, -1*lim_y-corner_marker_depth], color=outline_color,
              linewidth=outline_width, zorder=0)
    axes.plot([-1*lim_x, -1*lim_x-corner_marker_depth],
              [-1*corner_buffer_y, -1*corner_buffer_y], color=outline_color,
              linewidth=outline_width, zorder=0)
    # Add the top right corner distance markers
    axes.plot([corner_buffer_x, corner_buffer_x],
              [lim_y, lim_y+corner_marker_depth], color=outline_color,
              linewidth=outline_width, zorder=0)
    axes.plot([lim_x, lim_x+corner_marker_depth],
              [corner_buffer_y, corner_buffer_y], color=outline_color,
              linewidth=outline_width, zorder=0)
    # Add the bottom right corner distance markers
    axes.plot([corner_buffer_x, corner_buffer_x],
              [-1*lim_y, -1*lim_y-corner_marker_depth], color=outline_color,
              linewidth=outline_width, zorder=0)
    axes.plot([lim_x, lim_x+corner_marker_depth],
              [-1*corner_buffer_y, -1*corner_buffer_y], color=outline_color,
              linewidth=outline_width, zorder=0)

    axes.set_xlim(xmin, xmax)
    axes.set_ylim(ymin, ymax)
    axes.set_xlabel("x [meter]")
    axes.set_ylabel("y [meter]")


def msg_to_plot_data(msg, highlighted_players, team1_name, team2_name, ball_id):
    
    pos_df = pd.DataFrame(msg['pos'])

    ball_data = pos_df[pos_df['PlrID'] == ball_id]
    team1_data = pos_df[pos_df['TeamName'] == team1_name]
    team2_data = pos_df[pos_df['TeamName'] == team2_name]
    highlight_data = pos_df[pos_df['PlrID'].isin(highlighted_players)]

    return ball_data, team1_data, team2_data, highlight_data


def create_field_plot():

    fig, axes = plt.subplots(figsize=(9, 6))

    # Plot the entire field
    set_plot_area(axes, '#71AB47', '#FFFFFF', -60, 60, -40, 40)
    
    # Create the artists for the players and ball
    ball, = axes.plot([], [], "o", color="#000000", markersize=6, label='Ball')
    team1, = axes.plot([], [], "o", color="#3D42D4", markersize=9, label='Team 1')
    team2, = axes.plot([], [], "o", color="#F4252D", markersize=9, label='Team 2')
    highlight, = axes.plot([], [], "o", color="#000000", markersize=15, mfc="none", label='Func')

    # Plot a legend
    axes.legend(loc='upper right', bbox_to_anchor=(1.13, 1.05), fancybox=True, shadow=True)
    axes.set_aspect('auto')

    fig.canvas.draw()
    
    return fig, ball, team1, team2, highlight


def update_positions(fig, ball, team1, team2, highlight, data, highlighted_plr_ids):

    ball_data, team1_data, team2_data, highlight_data,  = \
        msg_to_plot_data(data, highlighted_plr_ids, 'Team 1', 'Team 2', 0)

    # Update the artists when any new data comes in
    ball.set_data(ball_data['X'], ball_data['Y'])
    team1.set_data(team1_data['X'], team1_data['Y'])
    team2.set_data(team2_data['X'], team2_data['Y'])
    highlight.set_data(highlight_data['X'], highlight_data['Y'])

    fig.canvas.draw()


def get_datastream():

    datastreamer = DataStreamer('modules/sample_dataset.csv', 'Timestamp')

    return datastreamer


def run_stream(datastream, func):

    fig, ball, team1, team2, highlight = create_field_plot()

    for data in datastream.local_stream():

        highlighted_ids = func(data)
        update_positions(fig, ball, team1, team2, highlight, data, highlighted_ids)

