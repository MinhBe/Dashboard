---
aliases: []
created: 2026-04-23 10:50:46
progress: raw
blueprint: []
impact: 
urgency: 
tags: []
category: []
---
# Generative Adversarial Network (GAN)

Last Updated : 14 Apr, 2026

GANs are models that generate new, realistic data by learning from existing data. Introduced by Ian Goodfellow in 2014, they enable machines to create content like images, videos and music.

![generative_adverarial_network_gans.webp](https://media.geeksforgeeks.org/wp-content/uploads/20251215095632135766/generative_adverarial_network_gans.webp)![generative_adverarial_network_gans.webp](https://media.geeksforgeeks.org/wp-content/uploads/20251215095632135766/generative_adverarial_network_gans.webp)

They are useful because:

- Create new data similar to real world data
- Go beyond classification to generate content
- Used in art, gaming, healthcare and data science

## Architecture of GAN

GAN consists of two neural networks the generator and the discriminator trained adversarially, where the generator tries to fool the discriminator and the discriminator tries to distinguish real from fake data.

### 1. Generator Model

The generator is a deep neural network that takes random noise as input to generate realistic data samples like images or text. It learns the underlying data patterns by adjusting its internal parameters during training through [backpropagation](https://www.geeksforgeeks.org/machine-learning/backpropagation-in-neural-network/). Its objective is to produce samples that the discriminator classifies as real.

****Generator Loss Function:**** The generator tries to minimize this loss:

> [Tex]J_{G} = -\frac{1}{m} \Sigma^m _{i=1} log D(G(z_{i}))[/Tex]

where

- [Tex]J_G[/Tex]measure how well the generator is fooling the discriminator.
- [Tex]G(z_i)[/Tex] is the generated sample from random noise [Tex]z_i[/Tex]
- [Tex]D(G(z_i))[/Tex] is the discriminator’s estimated probability that the generated sample is real.

The generator aims to maximize [Tex]D(G(z_i))[/Tex] meaning it wants the discriminator to classify its fake data as real (probability close to 1).

### 2. Discriminator Model

The discriminator is a binary classifier that distinguishes real data from generated samples. Through training, it refines its parameters to improve detection of fake data and when working with images, it uses convolutional layers to extract features and enhance classification accuracy.

****Discriminator Loss Function:**** The discriminator tries to minimize this loss:

> [Tex]J_{D} = -\frac{1}{m} \Sigma_{i=1}^m log\; D(x_{i}) - \frac{1}{m}\Sigma_{i=1}^m log(1 - D(G(z_{i}))[/Tex]

- [Tex]J_D[/Tex] measures how well the discriminator classifies real and fake samples.
- [Tex]x_{i}[/Tex] is a real data sample.
- [Tex]G(z_{i})[/Tex] is a fake sample from the generator.
- [Tex]D(x_{i})[/Tex] is the discriminator’s probability that [Tex]x_{i}[/Tex] is real.
- [Tex]D(G(z_{i}))[/Tex] is the discriminator’s probability that the fake sample is real.

The discriminator wants to correctly classify real data as real (maximize [Tex]log D(x_{i})[/Tex] and fake data as fake (maximize [Tex]log(1 - D(G(z_{i}))[/Tex])

### MinMax Loss

![GAN](https://media.geeksforgeeks.org/wp-content/uploads/20260320101654085537/GAN.webp "Click to enlarge")

GAN

GANs are trained using a [MinMax Loss](https://www.geeksforgeeks.org/dsa/minimax-algorithm-in-game-theory-set-1-introduction/) between the generator and discriminator:

> [Tex]min_{G}\;max_{D}(G,D) = [\mathbb{E}_{x∼p_{data}}[log\;D(x)] + \mathbb{E}_{z∼p_{z}(z)}[log(1 - D(g(z)))][/Tex]

where:

- [Tex]G [/Tex]is generator network and is [Tex]D[/Tex] is the discriminator network
- [Tex]p_{data}(x)[/Tex] = true data distribution
- [Tex]p_z(z) [/Tex]= distribution of random noise (usually normal or uniform)
- [Tex]D(x)[/Tex] = discriminator’s estimate of real data
- [Tex]D(G(z)) [/Tex]= discriminator’s estimate of generated data

The generator tries to minimize this loss (to fool the discriminator) and the discriminator tries to maximize it (to detect fakes accurately).

## ****Working of GAN****

GAN train by having two networks the Generator (G) and the Discriminator (D) compete and improve together. Here's the step-by-step process

### ****1. Generator's First Move****

The generator starts with a random noise vector like random numbers. It uses this noise as a starting point to create a fake data sample such as a generated image. The generator’s internal layers transform this noise into something that looks like real data.

### ****2. Discriminator's Turn****

The discriminator receives two types of data:

- Real samples from the actual training dataset.
- Fake samples created by the generator.

D's job is to analyze each input and find whether it's real data or something G cooked up. It outputs a probability score between 0 and 1. A score of 1 shows the data is likely real and 0 suggests it's fake.

### ****3. Adversarial Learning****

- If the discriminator correctly classifies real and fake data it gets better at its job.
- If the generator fools the discriminator by creating realistic fake data, it receives a positive update and the discriminator is penalized for making a wrong decision.

### ****4. Generator's Improvement****

- Each time the discriminator mistakes fake data for real, the generator learns from this success.
- Through many iterations, the generator improves and creates more convincing fake samples.

### ****5. Discriminator's Adaptation****

- The discriminator also learns continuously by updating itself to better spot fake data.
- This constant back-and-forth makes both networks stronger over time.

### ****6. Training Progression****

- As training continues, the generator becomes highly proficient at producing realistic data.
- Ideally, the generator improves to the point where the discriminator finds it difficult to distinguish real from generated data, although in practice GAN training can be unstable and may not always reach this balance.
- At this point, the generator can produce high quality synthetic data that can be used for different applications.

## Types of GAN

There are several types of GANs each designed for different purposes. Here are some important types:

### ****1. Vanilla GAN****

Vanilla GAN is the simplest type of GAN. It consists of:

- A generator and a discriminator both are built using multi-layer perceptrons (MLPs).
- The model optimizes its mathematical formulation using stochastic gradient descent (SGD).

While foundational, Vanilla GAN can face problems like:

- Generator produces limited types of outputs repeatedly.
- Generator and discriminator may not improve smoothly.

### ****2. Conditional GAN (CGAN)****

Conditional GAN (CGAN) adds an additional conditional parameter to guide the generation process. Instead of generating data randomly they allow the model to produce specific types of outputs.

Working of CGANs:

- A conditional variable (y) is fed into both the generator and the discriminator.
- This ensures that the generator creates data corresponding to the given condition (e.g generating images of specific objects).
- The discriminator also receives the labels to help distinguish between real and fake data.

****Example****: Instead of generating any random image, CGAN can generate a specific object like a dog or a cat based on the label.

### ****3. Deep Convolutional GAN (DCGAN)****

Deep Convolutional GAN (DCGAN) are among the most popular types of GANs used for image generation.

They are important because they:

- Uses Convolutional Neural Networks (CNNs) instead of simple multi-layer perceptrons (MLPs).
- Max pooling layers are replaced with convolutional stride helps in making the model more efficient.
- Fully connected layers are removed, which allows for better spatial understanding of images.

DCGANs are successful because they generate high-quality, realistic images.

### ****4. Laplacian Pyramid GAN (LAPGAN)****

Laplacian Pyramid GAN (LAPGAN) is designed to generate ultra-high-quality images by using a multi-resolution approach.

Working of LAPGAN:

- Uses multiple generator-discriminator pairs at different levels of the Laplacian pyramid.
- Images are first down sampled at each layer of the pyramid and upscaled again using Conditional GAN (CGAN).
- This process allows the image to gradually refine details and helps in reducing noise and improving clarity.

Due to its ability to generate highly detailed images, LAPGAN is considered a superior approach for photorealistic image generation.

### ****5. Super Resolution GAN (SRGAN)****

Super-Resolution GAN (SRGAN) is designed to increase the resolution of low-quality images while preserving details.

Working of SRGAN:

- Uses a deep neural network combined with an adversarial loss function.
- Enhances low-resolution images by adding finer details helps in making them appear sharper and more realistic.
- Helps to reduce common image upscaling errors such as blurriness and pixelation.


(4) Understanding GANs (Generative Adversarial Networks) - YouTube
https://www.youtube.com/watch?v=RAa55G-oEuk

Transcript:
(00:00) imagine you're a counterfeit and your objective is to sneak some fake money past the police if you're the police your aim is to accurately distinguish between this fake money and real money now due to this intense scrutiny by the police the counter fitter will end up producing fake money that very closely resembles the real money with the end goal of making them indistinguishable from one another in other words the counterfeit has to learn a generative model of real money now believe it or not such a simple idea has
(00:34) seen very successful application in the domain of machine learning where can be used to generate high quality synthetic examples of everything from images to speech this is the fundamental idea of the generative adversarial Network or Gan for short at its heart is a unique adversarial learning framework that pits a generative model which is our counterfeit against a discriminator which is our release the discriminator learns to classify real from generated samples and the generator tries to trick it by this competitive process the
(01:10) generator can eventually create samples that are realistic giving us a working generative model so in this video we're going to explain how this works we're first going to motivate the Gan by introducing the general problem of generative modeling and then explore how the Gan addresses this problem so what exactly is generative modeling well let's assume that we have some input data variable X and this could represent anything for example an image now imagine that we want to train a model that captures some Target distribution
(01:42) in the data space and this could correspond to any intended category like cats so in this example a successful generative model would be able to generate novel images of cats just by sampling from this learned distribution which we call pcats and it may also be able to perform things like anomaly detection when faced with images of things other than cats now more formally let's imagine that we have some data set D which is just a collection of points in our data space now we imagine that these points in our data space have been
(02:15) sampled from some underlying data distribution P star of X so P star of X here is essentially our ground truth generative procedure which gave rise to the samples in our data set in the first place now the problem is this procedure remains unknown to us so the best that we can do is try to approximate it by using some model P Theta where Theta are the model parameters so the basic goal of generative modeling is to optimize Theta such that our model distribution aligns as closely as possible to our Target distribution P star and to enable
(02:53) sufficient flexibility in our generative model we'd usually represent it using some kind of deep neural network on the face of it this problem looks pretty simple we can just spin up some arbitrarily powerful neural network and treat the neural network output as the probability of the input X however it turns out that the situation is a bit more complicated since if we want our neural network output to represent an actual probability distribution then we'll need it to satisfy two additional criteria first the inputs all need to be
(03:26) non- negative which is a condition of any probability it now we can easily solve this by just applying some kind of positively valued function f which could be something like an exponential on our neural network output however the second condition is a bit trickier and it basically says that our function needs to be normalized such that its integral over the entire space is equal to one and again this just stems from the definition of probability so if this integral happens to equal something else which we'll call Z
(04:01) then we'll have to normalize our output through division by Z Now the problem is that this integral is typically intractable to compute meaning that in general it does not have an analytical form and it'll also be very expensive to estimate by sampling if x has a high dimension now not being able to compute the normalization constant is a big problem because then if we optimize Theta to directly increase the numerator of our out output we can't actually be sure that we're increasing P of X overall since we may be increasing Z by
(04:37) an even greater amount without knowing so this issue of intractable normalization constants is one of the central problems of generative modeling now Gans sidestep this problem by essentially just reframing it now we're not really interested in directly learning the data distribution P star instead we indirectly learn it with the help of some latent VAR aable Z which aderes to a known probability distribution pz which is usually a gaussian or normal distribution so for this reason we'll call pz our noise distribution so the
(05:13) idea here is that since our latent distribution pz is definitely a probability distribution which is normalized and everything we can implicitly learn our Target distribution P Star by mapping points in latent space to points in data space such that our noise distribution in latent space maps onto our Target distribution in data space but of course the big challenge is to ensure that our mapping actually produces points from P star and that's where the Gan comes in so how does a gan work well basically as we've mentioned
(05:50) we have two models a generator model G and a discriminator Model D both typically built as deep neural networks our generator Maps our noise distribution in latent space to some generated distribution in data space PG which we want to align as closely as possible with our Target distribution P star in other words we want our generated samples to be indistinguishable from our real samples meanwhile it's the job of the discriminator to distinguish or discriminate between those two classes which are the real and generated inputs
(06:27) so our discriminator Model D takes as input our data variable X and outputs a single scalar DFX which we treat as the discriminator prediction of the probability that X is real rather than generated now in practice we limit the range of the discriminator output to somewhere between 0 and one and treat this as a standard binary classification problem and again we can choose any arbitrary neural network architecture that does the job so on the surface the training procedure of the Gan is actually pretty simple the discriminator
(07:02) performs some binary classification task between real and generated samples and the discriminator is trained to improve its own performance while the generator is trained to worsen it however the magic of the Gan is that this seemingly very simple training Dynamic can in fact push the generator to eventually create realistic looking samples to understand how this is possible let's first take a closer look at the exact form of the loss function used to train our Gan then see how it promotes the alignment of our
(07:34) generator distribution with our Target distribution so at the core of everything is our binary classification task the discriminator output is the probability of our sample being real so if our sample actually is real then the ground truth output is one and if it's generated then the ground truth output is zero so in essence both the discriminator output and the ground truth can be described as categorical distributions with only two categories real and generated and this is also known as a beri distribution so now the
(08:09) goal of the discriminator is to align these distributions using some appropriate loss function so let's derive it so to start off with the discriminator output D ofx can be used to define a conditional beri distribution over our class labels y similarly we have a ground truth conditional PB B for beri and this just assigns the class label so if x is real then yal 1 has a probability of 1 and if x is generated then yal 0 has a probability of one now if we want to align these two distributions as closely as possible we
(08:48) need a measure of closeness between the distributions and for this we use the coolback lier Divergence or KL Divergence between our two distributions now this Di convergence can be thought of as a measure of the distance between two distributions that being said it's not actually symmetric so in a way analogies with distance are a bit misleading but technically speaking the K Divergence of P star B from D is the relative entropy of the distribution p b if we assume that the distribution D is true and this is just calculated by an
(09:25) expected difference of logs over p b so this is just the general definition of the coolback LI Divergence and now if we want to calculate this expectation over discrete variables we can just use the following summation now since we just have a log of a fraction here we can actually split this summation like so now the neat thing is that our left hand term is actually constant with respect to D so we can just ignore it in our training objective which just becomes this and of course you may recognize this as just the cross entropy
(10:01) between p b and d now moving on our situation is actually made even more simple by the fact that we only have two classes or only two values of Y which are Z and one so our loss just reduces to these two terms now since all our distributions are beri distributions and since our D distribution just looks like this we can actually reexpress our loss like so which again we may recognize as the classic form of the binary cross entropy loss so our loss is just a binary cross entropy now to actually train our discriminator we just run it
(10:42) on a classification task using a mixed data set of real and generated samples the discriminator job now is to distinguish between these real and generated samples So intuitively speaking it has to detect those features of the input that give away the fact that something is not real therefore our final discriminator loss L of D is just the sum of the expected values of our binary cross entropy term over both the real and generated distributions now if x comes from P star then P star B of one becomes one and if
(11:20) x comes from PG then P star B of one becomes zero so we can simplify it to just this and of course we can rewrite this again in terms of our noise distribution P of Z so here we have our final discriminator loss now the only thing we're missing is our generator loss now of course the ultimate objective is to align PFG with P star but it turns out we can achieve this by using the intermediate objective of reducing the discriminator performance as much as possible so the generator loss is the negative of the discriminator loss just
(12:01) ignoring the first term uh since the generator can't actually influence this so basically what we have here is a situation where the generator and discriminator are being trained on directly contradictory objectives now in Game Theory speak we can think of this expression as some value function V that our generator is trying to minimize and our discriminator is trying to maximize so training can be framed as a two-player Zero Sum game or a minia Max game played by the generator and discriminator now this just means that
(12:36) they're involved in a competitive scenario where each player's payoff is the opposite of the other players's payoff and where they each seek to maximize their own payoff under the constraint that their opponent is seeking to do the same so the minia max framework applies here because the generator is trying to minimize the value function whilst the discriminator is trying to maximize it now as it turns out this simple game theoretic framework is sufficient to push our generator distribution to the Target distribution
(13:07) given that our models are sufficiently powerful and that we allow for sufficient training time now this is actually quite a remarkable result so we'll spend the next few minutes proving it to start off we recognize that training our Gan is equivalent to finding a Nash equilibrium of our game this is when neither the generator nor the discriminator can decrease its loss by changing its parameters assuming that the other model keeps its parameters constant now this is an equilibrium because it means that our model
(13:38) parameters are stable so let's see what it takes to achieve this equilibrium our strategy will be as follows first we're going to find an expression for the optimal discriminator given any particular generator and we're going to call this D star so in other words given some generator G this is the ideal configuration for D that minimizes the discriminator loss second we're going to find the optimal generator assuming that our discriminator remains optimal throughout the entire process now remember that our goal is to
(14:17) prove that if we train both our models to optimality then PG is going to align with P star okay so in order to find our optimal discriminator let's start by taking our value function and expanding out the expectations to integrals and of course we could just rewrite this as one big integral over X now if we're the discriminator we want to find some optimal DX such that we maximize this entire integral one way we can do that is to actually just maximize the expression inside the integral which turns out to be valid in our situation
(14:53) and this is quite feasible to do so as a first step to find the maximum we just take the the derivative of this expression with respect to D ofx and here we're just treating P star and PG as constants then once we have our result we can equate it to zero to find a Stationary point and if we work through the algebra we'll find that the stationary Point looks like this and it turns out that the second derivative here is also negative so we know that it's a maximum point which is therefore an expression for our optimal
(15:28) discrimination D star given any generator G so now that we have our first result let's find our optimal generator given our optimal discriminator so here we assume that our discriminator remains optimal as the generator also optimizes now given that our discriminator remains optimal our value function basically just boils down to a function of just our generator which we call our generator Criterion C now to get this we just just substitute our expression for D star of g into our value function which just gives us
(16:06) this now as the generator we're interested in minimizing this Criterion the first step is to realize through some clever working that what we actually have here is the sum of two KL divergences where we recall the definition of KL Divergence as the expected difference of logs now being The Savvy statisticians we are we can also recognize this as 2 times What's called the Yensen Shannon Divergence between P star and PG where this Divergence is just half the sum of K divergences with some reference distribution M now this is quite neat
(16:48) because we've just shown that optimizing the generator assuming an optimal discriminator is just equivalent to minimizing the yens and Shana Divergence between our two distributions p R and PG now this Divergence is non- negative so it has a minimum value of zero and it reaches this value precisely and only when P star and PG are equal so we've effectively shown that minimizing the generator loss is equivalent to our lining our Target and Generator distributions at which point the Criterion function becomes minus log
(17:25) 4 so our theoretical analysis has shown why our Gans is system should optimize to as equilibrium with PG aligning with P star however of course the real world is quite a bit Messier and both our generator and discriminator are real neuron networks with non-infinite expressibility so when optimizing in parameter space we may fall into local Minima and other issues may also prevent us from reaching and stabilizing a global Optimum so it turns out that in the real world training a again is not so straight forward so on that note let's first take
(18:02) a look at what should be happening as we train our Gan then focus on some of the potential pitfalls that might plague our training so imagine that we have a one-dimensional x now in the initial stage of our analysis we have our generator and discriminator and they're both kind of near convergence so PG is not so far off from P star and D is not so far off from D but they haven't reached them yet now in the second stage our discriminator reaches convergence so D equals D star of G but our generator hasn't converged yet so here we're
(18:38) making the assumption that the discriminator reaches convergence more quickly than the generator which also happens to align with the analysis we showed earlier now in the second stage our discriminator converges so it has a high discriminative capacity and thus becomes useful to the generator in guiding it towards P star which is the third stage then finally in the fourth stage PFG becomes P star and our discriminator output becomes 1/2 everywhere so in a perfect world this is what should happen during Gan training and we should
(19:15) eventually reach convergence or the Nash equilibrium of our Minimax game without discriminator being completely confused between real and generated samples but of course the real world is not so simple so now we're going to look at three potential training issues that can upset this nice story the optimal and lousy discriminator problem the possibility of non-con convergence and the possibility of mode collapse so first of all why might an optimal discriminator be problematic especially as we've just used it to show that it can help the
(19:52) generator reach convergence well it turns out that during Gan training as our discriminator approaches optimal State the gradients of our generator parameters Theta begin to vanish in other words as the discriminator gets too good it can no longer transmit useful information to the generator you can actually derive this result through some mathematical analysis which I won't show here but I'll link the relevant paper in the description below now this is certainly a big problem because having an optimal discriminator is what guarantees that a
(20:27) generator loss is close to the yens and Shannon Divergence yet if our discriminator really is optimal in the real world then our model as a whole can remain stuck due to this problem of Vanishing gradients Now to S side step this issue the original authors suggest using a modified generator loss function but it turns out that if we modify it like so then we'll face the problem of Highly unstable gradients so in other words whatever our choice Gan train tring is difficult now somewhat related to this is what we can call the problem of the
(21:04) lousy discriminator where the generator updates too quickly for our discriminator to keep up and as a consequence the discriminator again cannot transmit useful information to the generator because now it's too confused the problem here is that if the discriminator is junk then the generator which relies on it will also start producing junk and our Gan never stay stabilizes to a good state so essentially we need to regulate our discriminator such that it's good but not too good and in practice this can be achieved in several ways for example in
(21:41) Gan training it's quite common to alternate between discriminator and Generator training steps and to allow for the discriminator to take K steps for every one step that the generator takes where K is a hyperparameter another thing we could also do is set the learning rate for the discriminated parameters to be higher than that for the generated parameters so using methods like these we can actually control the degree to which the discriminator reaches optimality now yet another problem we have to worry about is the possibility
(22:18) of non-con convergence as we've seen this can happen if we have a lousy discriminator but it it can also happen as a general feature of our training situation and this is is because not all Mini Max Games necessarily converge to imagine how this can happen consider the following hypothetical scenario we have only two model parameters X and Y we also have two players so player a minimizes the loss function XY with respect to X and player B minimizes the loss function - XY with respect to Y therefore the gradient of
(22:59) parameter X will be Y and the gradient of parameter y will be - x now we can see that there's an equilibrium at the point x = y = 0 but it's also possible that our parameters may never converge to the solution if we alternate between optimizing A and B for example if we find ourselves anywhere on this box then we're just going to trace the outline of the Box in per uity following a stable orbit instead of ever converging to an equilibrium point so in a nutshell this is the problem of non-con convergence now a third notorious
(23:42) problem with Gans is when the generator actually learns to achieve good performance by just mapping every noise Vector to the same point in data space so even if the generator succeeds in producing realistic outputs it is clearly failed in the overarching goal of approximating our data distribution however a generator may very well come to rely on this strategy as a way of confusing the discriminator and reducing its own loss just by producing the same output every time which it knows to be a pretty good bet now this is a common
(24:18) problem in Gans and it's usually referred to as mode collapse because in generative modeling we're trying to capture the modes of a target distribution but in the this case we're capturing just one of these modes now one way of interpreting what's happening is this so imagine that over the space of our data X is a landscape of values D of X that determine the discriminator prediction now if you have some generator outputs in a batch sufficiently close to each other then our generator gradient updates May push
(24:53) these points to the same point which the discriminator deems as highly realistic now of course the discriminator can then adapt and realize that these points are generated which we can visualize as a shifting of the contour map but then when the generated points move due to the gradient update they all move together and so what we have is a cluster of generated points that will continue to all look the same now mode collapse is a notorious issue in Gan training but thankfully over the years people have created several
(25:28) Solutions to address this one such technique is called mini batch discrimination which without going into the details basically gives the discriminator information about every sample in a batch as it evaluates each individual sample this way the discriminator can learn to detect that points are being generated when they all happen to be very close to one another and so this reduces the effectiveness of the strategy of just producing one output even if it is highly realistic yet another approach is the vasin Gan which is an alternative Gan
(26:06) framework introduced to address problems such as mode collapse and training instability but that's beyond the scope of this video so here are a few common failure modes and as we've seen they can be very difficult to address because they are in a sense emergent outcomes of a stochastic training process and they show that while the Gan framework is simple on the Sur surface actually training again is anything but simple so this is probably a good place to end our introduction of ganss to sum up these models use an elegant adversarial
(26:39) framework to achieve impressive results in generative modeling but as we've seen they can also be tricky to train


(4) What are GANs (Generative Adversarial Networks)? - YouTube
https://www.youtube.com/watch?v=TpMIssRdhco

Transcript:
(00:01) One of my favorite machine learning algorithms is Generative Adversarial Networks, or GAN. It pits two AI models off against each other, hence the "adversarial" part. Now, most machine learning models are used to generate a prediction. So we start with some input training data. And we feed that into our model.
(00:31) A model then makes a prediction in the form of output. And we can compare the predicted output with the expected output from the training data set. And then based upon that expected output and the actual predicted output, we can figure out how we should update our model to create better outputs. That is an example of supervised learning.
(01:10) A GAN is an example of unsupervised learning, it effectively supervises itself, and it consists of two submodels. So we have a generator submodel. And we have a discriminator submodel. Now, the generator's job is to create fake input or fake samples. And the discriminator's job is to take a given sample and figure out if it is a fake sample or if it's a real sample from the domain.
(02:13) And therein lies the adversarial nature of this. We have a generator creating fake samples and sending them to a discriminator. The discriminator is taking a look at a given sample and figuring out, "Is this a fake sample from the generator? Or is this a real sample from the domain set?" Now, this sort of scenario is often applied in image generation.
(02:42) There are images all over the internet of generators that have been used to create fake 3D models, fake faces, fake cats and so forth. So this really works by the generator iterating through a number of different cycles of creating samples, updating its model and so forth until it can create a sample that is so convincing that it can fool a discriminator and also fool us humans as well.
(03:14) So let's let's take an example of how this works with, let's say, a flower. So we are going to train a generator to create really convincing fake flowers, and the way that we start by doing this is we need to, first of all, train our discriminator model to recognize what a picture of a flower looks like.
(03:37) So our domain is lots of pictures of flowers, and we will be feeding this into the discriminator model and telling it to look at all of the attributes that make up those flower images. Take a look at the colors, the shading, the shapes and so forth. And when our discriminator gets good at recognizing real flowers, then we'll feed in some shapes that are not flowers at all.
(04:00) And make sure that it can discriminate those as being not-flowers. Now, this whole time our generator here was frozen, it wasn't doing anything. But we're our discriminator gets good enough at recognizing things from our domain, then we apply our generator to start creating fake versions of those things.
(04:21) So a generator is going to take a random input vector and it is going to use that to create its own fake flower. Now, this fake flower image is sent to the discriminator, and now the discriminator has a decision to make: is that image of a flower the real thing from the domain, or is it a fake from the generator? Now, the answer is revealed to both the generator and the discriminator.
(04:57) The flower was fake and based upon that, the generator and discriminator will change their behavior. This is a zero sum game, there's always a winner and a loser. The winner gets to remain blissfully unchanged. Their model doesn't change at all, whereas the loser has to update their model. So if the discriminator successfully spotted that this flower was a fake image, then lead discriminator remains unchanged.
(05:27) But the generator will need to change its model to generate better fakes. Whereas if the reverse is true and the generator is creating something that fools the discriminator, the discriminator model will need to be updated itself in order to better be able to tell where we have a fake sample coming in, so it's fooled less easily.
(05:50) And that's basically how these things work, and we go through many, many iterations of this until the generator gets so good that the discriminator can no longer pick out its fakes. And there we have built a very successful generator to do whatever it is we wanted it to do. Now, often in terms of images, the generator and the discriminator implemented as CNNs.
(06:19) These are Convolutional Neural Networks. CNN's are a great way of recognizing patterns in image data and entering into sort of the area of object identification. We have a whole separate video on CNNs, but they're a great way to really implement the generator and discriminator in this scenario. But the  whole process of a GAN, isn't just to create really good fake flowers or fake cat images for the internet.
(06:50) You can apply it to all sorts of use cases. So take, for example, video frame prediction. If we fit in a particular frame of video from a camera, we can use a GAN to predict what the next frame in this sequence will look like. This is a great way to be able to predict what's going to happen in the immediate future and might be used, for example, in a surveillance system.
(07:16) If we can figure out what is likely to happen next, we can take some action based upon that. There's also other things you can do, like image enhancement. So if we have a kind of a low resolution image, we can use a GAN to create a much higher resolution version of the image by figuring out what each individual pixel is and then creating a higher resolution version of that.
(07:39) And we can even go as far as using this for things that are not related to images at all, like encryption. But we can create a secure encryption algorithm that can be decrypted and encrypted by the sender and receiver, but cannot be easily intercepted, again by going through these GAN iterations to create a really good generator.
(07:59) So that's GAN. It's the battle of the bots where you can take your young, impressionable and unchanged generator and turn it into a master of forgery. If you have any questions, please drop us a line below. And if you want to see more videos like this in the future, please like and subscribe.



(4) What are GANs (Generative Adversarial Networks)? - YouTube
https://www.youtube.com/watch?v=TpMIssRdhco

Transcript:
(00:01) One of my favorite machine learning algorithms is Generative Adversarial Networks, or GAN. It pits two AI models off against each other, hence the "adversarial" part. Now, most machine learning models are used to generate a prediction. So we start with some input training data. And we feed that into our model.
(00:31) A model then makes a prediction in the form of output. And we can compare the predicted output with the expected output from the training data set. And then based upon that expected output and the actual predicted output, we can figure out how we should update our model to create better outputs. That is an example of supervised learning.
(01:10) A GAN is an example of unsupervised learning, it effectively supervises itself, and it consists of two submodels. So we have a generator submodel. And we have a discriminator submodel. Now, the generator's job is to create fake input or fake samples. And the discriminator's job is to take a given sample and figure out if it is a fake sample or if it's a real sample from the domain.
(02:13) And therein lies the adversarial nature of this. We have a generator creating fake samples and sending them to a discriminator. The discriminator is taking a look at a given sample and figuring out, "Is this a fake sample from the generator? Or is this a real sample from the domain set?" Now, this sort of scenario is often applied in image generation.
(02:42) There are images all over the internet of generators that have been used to create fake 3D models, fake faces, fake cats and so forth. So this really works by the generator iterating through a number of different cycles of creating samples, updating its model and so forth until it can create a sample that is so convincing that it can fool a discriminator and also fool us humans as well.
(03:14) So let's let's take an example of how this works with, let's say, a flower. So we are going to train a generator to create really convincing fake flowers, and the way that we start by doing this is we need to, first of all, train our discriminator model to recognize what a picture of a flower looks like.
(03:37) So our domain is lots of pictures of flowers, and we will be feeding this into the discriminator model and telling it to look at all of the attributes that make up those flower images. Take a look at the colors, the shading, the shapes and so forth. And when our discriminator gets good at recognizing real flowers, then we'll feed in some shapes that are not flowers at all.
(04:00) And make sure that it can discriminate those as being not-flowers. Now, this whole time our generator here was frozen, it wasn't doing anything. But we're our discriminator gets good enough at recognizing things from our domain, then we apply our generator to start creating fake versions of those things.
(04:21) So a generator is going to take a random input vector and it is going to use that to create its own fake flower. Now, this fake flower image is sent to the discriminator, and now the discriminator has a decision to make: is that image of a flower the real thing from the domain, or is it a fake from the generator? Now, the answer is revealed to both the generator and the discriminator.
(04:57) The flower was fake and based upon that, the generator and discriminator will change their behavior. This is a zero sum game, there's always a winner and a loser. The winner gets to remain blissfully unchanged. Their model doesn't change at all, whereas the loser has to update their model. So if the discriminator successfully spotted that this flower was a fake image, then lead discriminator remains unchanged.
(05:27) But the generator will need to change its model to generate better fakes. Whereas if the reverse is true and the generator is creating something that fools the discriminator, the discriminator model will need to be updated itself in order to better be able to tell where we have a fake sample coming in, so it's fooled less easily.
(05:50) And that's basically how these things work, and we go through many, many iterations of this until the generator gets so good that the discriminator can no longer pick out its fakes. And there we have built a very successful generator to do whatever it is we wanted it to do. Now, often in terms of images, the generator and the discriminator implemented as CNNs.
(06:19) These are Convolutional Neural Networks. CNN's are a great way of recognizing patterns in image data and entering into sort of the area of object identification. We have a whole separate video on CNNs, but they're a great way to really implement the generator and discriminator in this scenario. But the  whole process of a GAN, isn't just to create really good fake flowers or fake cat images for the internet.
(06:50) You can apply it to all sorts of use cases. So take, for example, video frame prediction. If we fit in a particular frame of video from a camera, we can use a GAN to predict what the next frame in this sequence will look like. This is a great way to be able to predict what's going to happen in the immediate future and might be used, for example, in a surveillance system.
(07:16) If we can figure out what is likely to happen next, we can take some action based upon that. There's also other things you can do, like image enhancement. So if we have a kind of a low resolution image, we can use a GAN to create a much higher resolution version of the image by figuring out what each individual pixel is and then creating a higher resolution version of that.
(07:39) And we can even go as far as using this for things that are not related to images at all, like encryption. But we can create a secure encryption algorithm that can be decrypted and encrypted by the sender and receiver, but cannot be easily intercepted, again by going through these GAN iterations to create a really good generator.
(07:59) So that's GAN. It's the battle of the bots where you can take your young, impressionable and unchanged generator and turn it into a master of forgery. If you have any questions, please drop us a line below. And if you want to see more videos like this in the future, please like and subscribe.


(4) What are GANs (Generative Adversarial Networks)? - YouTube
https://www.youtube.com/watch?v=TpMIssRdhco

Transcript:
(00:01) One of my favorite machine learning algorithms is Generative Adversarial Networks, or GAN. It pits two AI models off against each other, hence the "adversarial" part. Now, most machine learning models are used to generate a prediction. So we start with some input training data. And we feed that into our model.
(00:31) A model then makes a prediction in the form of output. And we can compare the predicted output with the expected output from the training data set. And then based upon that expected output and the actual predicted output, we can figure out how we should update our model to create better outputs. That is an example of supervised learning.
(01:10) A GAN is an example of unsupervised learning, it effectively supervises itself, and it consists of two submodels. So we have a generator submodel. And we have a discriminator submodel. Now, the generator's job is to create fake input or fake samples. And the discriminator's job is to take a given sample and figure out if it is a fake sample or if it's a real sample from the domain.
(02:13) And therein lies the adversarial nature of this. We have a generator creating fake samples and sending them to a discriminator. The discriminator is taking a look at a given sample and figuring out, "Is this a fake sample from the generator? Or is this a real sample from the domain set?" Now, this sort of scenario is often applied in image generation.
(02:42) There are images all over the internet of generators that have been used to create fake 3D models, fake faces, fake cats and so forth. So this really works by the generator iterating through a number of different cycles of creating samples, updating its model and so forth until it can create a sample that is so convincing that it can fool a discriminator and also fool us humans as well.
(03:14) So let's let's take an example of how this works with, let's say, a flower. So we are going to train a generator to create really convincing fake flowers, and the way that we start by doing this is we need to, first of all, train our discriminator model to recognize what a picture of a flower looks like.
(03:37) So our domain is lots of pictures of flowers, and we will be feeding this into the discriminator model and telling it to look at all of the attributes that make up those flower images. Take a look at the colors, the shading, the shapes and so forth. And when our discriminator gets good at recognizing real flowers, then we'll feed in some shapes that are not flowers at all.
(04:00) And make sure that it can discriminate those as being not-flowers. Now, this whole time our generator here was frozen, it wasn't doing anything. But we're our discriminator gets good enough at recognizing things from our domain, then we apply our generator to start creating fake versions of those things.
(04:21) So a generator is going to take a random input vector and it is going to use that to create its own fake flower. Now, this fake flower image is sent to the discriminator, and now the discriminator has a decision to make: is that image of a flower the real thing from the domain, or is it a fake from the generator? Now, the answer is revealed to both the generator and the discriminator.
(04:57) The flower was fake and based upon that, the generator and discriminator will change their behavior. This is a zero sum game, there's always a winner and a loser. The winner gets to remain blissfully unchanged. Their model doesn't change at all, whereas the loser has to update their model. So if the discriminator successfully spotted that this flower was a fake image, then lead discriminator remains unchanged.
(05:27) But the generator will need to change its model to generate better fakes. Whereas if the reverse is true and the generator is creating something that fools the discriminator, the discriminator model will need to be updated itself in order to better be able to tell where we have a fake sample coming in, so it's fooled less easily.
(05:50) And that's basically how these things work, and we go through many, many iterations of this until the generator gets so good that the discriminator can no longer pick out its fakes. And there we have built a very successful generator to do whatever it is we wanted it to do. Now, often in terms of images, the generator and the discriminator implemented as CNNs.
(06:19) These are Convolutional Neural Networks. CNN's are a great way of recognizing patterns in image data and entering into sort of the area of object identification. We have a whole separate video on CNNs, but they're a great way to really implement the generator and discriminator in this scenario. But the  whole process of a GAN, isn't just to create really good fake flowers or fake cat images for the internet.
(06:50) You can apply it to all sorts of use cases. So take, for example, video frame prediction. If we fit in a particular frame of video from a camera, we can use a GAN to predict what the next frame in this sequence will look like. This is a great way to be able to predict what's going to happen in the immediate future and might be used, for example, in a surveillance system.
(07:16) If we can figure out what is likely to happen next, we can take some action based upon that. There's also other things you can do, like image enhancement. So if we have a kind of a low resolution image, we can use a GAN to create a much higher resolution version of the image by figuring out what each individual pixel is and then creating a higher resolution version of that.
(07:39) And we can even go as far as using this for things that are not related to images at all, like encryption. But we can create a secure encryption algorithm that can be decrypted and encrypted by the sender and receiver, but cannot be easily intercepted, again by going through these GAN iterations to create a really good generator.
(07:59) So that's GAN. It's the battle of the bots where you can take your young, impressionable and unchanged generator and turn it into a master of forgery. If you have any questions, please drop us a line below. And if you want to see more videos like this in the future, please like and subscribe.


(4) What are GANs (Generative Adversarial Networks)? - YouTube
https://www.youtube.com/watch?v=TpMIssRdhco

Transcript:
(00:01) One of my favorite machine learning algorithms is Generative Adversarial Networks, or GAN. It pits two AI models off against each other, hence the "adversarial" part. Now, most machine learning models are used to generate a prediction. So we start with some input training data. And we feed that into our model.
(00:31) A model then makes a prediction in the form of output. And we can compare the predicted output with the expected output from the training data set. And then based upon that expected output and the actual predicted output, we can figure out how we should update our model to create better outputs. That is an example of supervised learning.
(01:10) A GAN is an example of unsupervised learning, it effectively supervises itself, and it consists of two submodels. So we have a generator submodel. And we have a discriminator submodel. Now, the generator's job is to create fake input or fake samples. And the discriminator's job is to take a given sample and figure out if it is a fake sample or if it's a real sample from the domain.
(02:13) And therein lies the adversarial nature of this. We have a generator creating fake samples and sending them to a discriminator. The discriminator is taking a look at a given sample and figuring out, "Is this a fake sample from the generator? Or is this a real sample from the domain set?" Now, this sort of scenario is often applied in image generation.
(02:42) There are images all over the internet of generators that have been used to create fake 3D models, fake faces, fake cats and so forth. So this really works by the generator iterating through a number of different cycles of creating samples, updating its model and so forth until it can create a sample that is so convincing that it can fool a discriminator and also fool us humans as well.
(03:14) So let's let's take an example of how this works with, let's say, a flower. So we are going to train a generator to create really convincing fake flowers, and the way that we start by doing this is we need to, first of all, train our discriminator model to recognize what a picture of a flower looks like.
(03:37) So our domain is lots of pictures of flowers, and we will be feeding this into the discriminator model and telling it to look at all of the attributes that make up those flower images. Take a look at the colors, the shading, the shapes and so forth. And when our discriminator gets good at recognizing real flowers, then we'll feed in some shapes that are not flowers at all.
(04:00) And make sure that it can discriminate those as being not-flowers. Now, this whole time our generator here was frozen, it wasn't doing anything. But we're our discriminator gets good enough at recognizing things from our domain, then we apply our generator to start creating fake versions of those things.
(04:21) So a generator is going to take a random input vector and it is going to use that to create its own fake flower. Now, this fake flower image is sent to the discriminator, and now the discriminator has a decision to make: is that image of a flower the real thing from the domain, or is it a fake from the generator? Now, the answer is revealed to both the generator and the discriminator.
(04:57) The flower was fake and based upon that, the generator and discriminator will change their behavior. This is a zero sum game, there's always a winner and a loser. The winner gets to remain blissfully unchanged. Their model doesn't change at all, whereas the loser has to update their model. So if the discriminator successfully spotted that this flower was a fake image, then lead discriminator remains unchanged.
(05:27) But the generator will need to change its model to generate better fakes. Whereas if the reverse is true and the generator is creating something that fools the discriminator, the discriminator model will need to be updated itself in order to better be able to tell where we have a fake sample coming in, so it's fooled less easily.
(05:50) And that's basically how these things work, and we go through many, many iterations of this until the generator gets so good that the discriminator can no longer pick out its fakes. And there we have built a very successful generator to do whatever it is we wanted it to do. Now, often in terms of images, the generator and the discriminator implemented as CNNs.
(06:19) These are Convolutional Neural Networks. CNN's are a great way of recognizing patterns in image data and entering into sort of the area of object identification. We have a whole separate video on CNNs, but they're a great way to really implement the generator and discriminator in this scenario. But the  whole process of a GAN, isn't just to create really good fake flowers or fake cat images for the internet.
(06:50) You can apply it to all sorts of use cases. So take, for example, video frame prediction. If we fit in a particular frame of video from a camera, we can use a GAN to predict what the next frame in this sequence will look like. This is a great way to be able to predict what's going to happen in the immediate future and might be used, for example, in a surveillance system.
(07:16) If we can figure out what is likely to happen next, we can take some action based upon that. There's also other things you can do, like image enhancement. So if we have a kind of a low resolution image, we can use a GAN to create a much higher resolution version of the image by figuring out what each individual pixel is and then creating a higher resolution version of that.
(07:39) And we can even go as far as using this for things that are not related to images at all, like encryption. But we can create a secure encryption algorithm that can be decrypted and encrypted by the sender and receiver, but cannot be easily intercepted, again by going through these GAN iterations to create a really good generator.
(07:59) So that's GAN. It's the battle of the bots where you can take your young, impressionable and unchanged generator and turn it into a master of forgery. If you have any questions, please drop us a line below. And if you want to see more videos like this in the future, please like and subscribe.