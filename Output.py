import pygame
import pandas
from pygame.locals import *
import sys

def main(df, clusterRoutes, times, clusters):
    pygame.init()
    SCALE = 24
    screen = pygame.display.set_mode([SCALE*84, SCALE*84])
    screen.fill((255, 255, 255))
    colors = [(200, 0, 0), (0, 200, 0), (0, 0, 200), (0, 200, 200), (200, 200, 0), (200, 0, 200)]
    for i in range(0, clusters):
        #Draw Routes
        n = 0
        pygame.draw.line(screen, colors[i],
                         (df.iloc[clusterRoutes[i][n][0] - 1].XCord * SCALE, df.iloc[clusterRoutes[i][n][0] - 1].YCord * SCALE),
                         (df.iloc[0].XCord * SCALE, df.iloc[0].YCord * SCALE), width=int(SCALE/3))
        for n in range(1, len(clusterRoutes[i])):
            pygame.draw.line(screen, colors[i],
                             (df.iloc[clusterRoutes[i][n-1][0] - 1].XCord * SCALE, df.iloc[clusterRoutes[i][n-1][0] - 1].YCord * SCALE),
                             (df.iloc[clusterRoutes[i][n][0] - 1].XCord * SCALE, df.iloc[clusterRoutes[i][n][0] - 1].YCord * SCALE), width=int(SCALE/3))
    for i in range(0, clusters):
        #Draw Nodes
        cluster = df[df.cluster == i]
        for n in range(0, cluster.shape[0]):
            if (cluster.iloc[n].Customer == 1):
                pygame.draw.circle(screen, (0,0,0), (cluster.iloc[n].XCord * SCALE, cluster.iloc[n].YCord * SCALE), int(SCALE*3), int(SCALE/2))
                pygame.draw.circle(screen, (255,255,255), (cluster.iloc[n].XCord * SCALE, cluster.iloc[n].YCord * SCALE), int(SCALE*2.5))
            else:
                pygame.draw.circle(screen, colors[i], (cluster.iloc[n].XCord * SCALE, cluster.iloc[n].YCord * SCALE), SCALE*1.25, int(SCALE/2))
                pygame.draw.circle(screen, (255,255,255), (cluster.iloc[n].XCord * SCALE, cluster.iloc[n].YCord * SCALE), SCALE*1)
    return screen

if __name__ == "__main__":
    main()