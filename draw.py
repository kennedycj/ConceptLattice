import matplotlib.pyplot as plt
import numpy as np

def graph(RM,names,deltaY=1,**kwargs):

    # Create figure
    ax=plt.subplot(1,1,1)

    for i in range(0, len(RM)):

        # Grab current intervals
        c1= (RM[i].lower, RM[i].upper)

        # Create y-values and shift intervals up by (i+1)*deltaY
        y=(i+1)*deltaY*np.ones((2,1))

        # Draw
        print(f"c1 = {c1}")
        if c1[0] == c1[1]:
            ax.plot([c1[0]],[i*deltaY],'o',**kwargs)
        if c1[0] < c1[1]:
            ax.plot(c1,y,**kwargs)
        if c1[0] > c1[1]:
            #ax.plot(c1,y,lw=lw,**kwargs)
            raise TypeError('interval start > end')

        midpoint = c1[0] + (c1[1] - c1[0]) / 2
        print(f"midpoint = {midpoint}")
        print(f"y = {y}")
        ax.annotate(names[i], xy=(midpoint, y[0]))
    # Set ylim so it looks nice
    ax.set_ylim([0,deltaY*(i+2)])

    return ax

# Define intervals
#intervals=np.array([(2,3),(2,4),(5,5),(1,3)])


# Plot
#graph(intervals,lw=5,c='b')

# Draw
#plt.show()