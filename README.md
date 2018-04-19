# animatelifempi.py
Goals:
Create a parallel version of Conway’s Game of Life with cylindrical boundary conditions. The top of the grid should wrap around to the bottom of the grid so that cells at the top and bottom of the grid can exchange information.
Steps:
1. Implement a parallel Game of Life without cylindrical boundary conditions, similar to the Relaxation solution. (one week from today).
2. Feel free to work on your own computer for this part if you wish. If you run on Colonial One, be sure to remove or comment out the parts of the code which create mp4s. If need be, your TAs and I can help set up DSRL for visualization.
3. Create a flowchart that illustrates the overall flow of the final product and what decisions are required. (see the next slide for a reminder).
4. Implement the final product with cylindrical boundaries (top/bottom).
5. Estimate and then experiment to find the largest grid (rows vs columns) that can be analyzed on one c1exp node on Colonial One using 16 workers. 
6. Submit jobs to a single node on c1exp on Colonial One and for probability values of 0.2, 0.4, 0.5, 0.75, & 0.9. Work in your /group/dats6402_10/netid directory.
7. Reimplement the parallel version using the acorn as a starting condition. I will provide the acorn starting conditions after completion of step 3. 
