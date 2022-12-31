
* Experiment 1:
In the first experiment the model from the lesson was used but with a few small modifications. The modifications were:
- Input dimensions: The input dimensions were changed to the shape of the images after resizing.
- The output: The output still has a relu activation, but the number of neurons is the number of possible classes.
The results of this model were not very good. (accuracy: 0.0574) The model may not be extracting the characteristics necessary for the classification, or maybe the hidden hidden layer with neurons are not enought to fit with the non-linearity of the data.
As solution the experiments 2, 3 and 4 will increese the number of convolutional layers, neuron's layers and both.

* Experiment 2:
In this second experiment, a layer with 256 neurons and relu activation was added. this layer was located just after finishing the convolutional layers and the flatten process.
The results of adding this layer are significantly better in relation to experiment 1 since the accuracy increased from 0.0574 for experiment 1 to 0.9067 in experiment 2.

* Experiment 3:
The third experiment consists of an architecture like the original used in experiment 1, but adding 2 layers. 
- 2D convolution: A first convolutional layer with 64 3x3 filters and relu activation. 
- Pooling: And a second layer of max-pooling to reduce the dimensionality of the extracted features.
The result was an accuracy of: 0.2557

* Experiment 4:
In this experiment the architecture of experiment 2 was used, but adding 2 layers after the first 2D convolution and maxpooling. 
- A convolutional layer with a 3 x 3 kernel, relu activation and 64 filters.
- Pooling: A 2 x 2 max-pooling layer to reduce the dimensions of the image.
As a result the accuracy increased to a final accuracy of 0.9803

* Conclusion:
In the experiments model of experiment 4 has a good enough accuracy of: 0.9803. The final architecture is:

Input:
- Images of IMG_WIDTH x IMG_HEIGHT x 3

Convolutional layers:
- 2D convolutional layer with 32 filters of 3x3 and relu activation
- Max-pooling layer of 2x2
- 2D convolutional layer with 64 filters of 3x3 and relu activation
- Max-pooling layer of 2x2

Then a flatten stage

Neuron Layers:
- Dense layer with 256 neurons and relu activation
- Dense layer with 128 neurons and relu activation
- Dropout of 0.5

Output:
- Dense layer with number of neurons as number of possible classes and softmax activation

* Note: The result of accuracy varies in each compilation. This possibly due to the fact that the weights of the neural network are started randomly which means that without the use of a seed each training initial weights will be different.