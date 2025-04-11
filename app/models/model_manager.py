"""
Model Manager Module

This module provides a unified interface for working with different AI models,
with a focus on Hugging Face models for text generation and classification.
"""
import os
from typing import Dict, List, Any, Optional, Union

from app.utils.logger import get_logger

# Import conditionally to handle missing dependencies gracefully
TRANSFORMERS_AVAILABLE = False
TORCH_AVAILABLE = False

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    pass

if TORCH_AVAILABLE:
    try:
        from transformers import (
            AutoModelForSequenceClassification,
            AutoModelForCausalLM,
            AutoTokenizer,
            pipeline
        )
        TRANSFORMERS_AVAILABLE = True
    except (ImportError, RuntimeError):
        pass

logger = get_logger(__name__)

class ModelManager:
    """
    Manages the loading, caching, and inference for various AI models.

    This class provides a unified interface for working with different models,
    primarily focusing on Hugging Face models for text tasks.
    """

    def __init__(self, model_name: str):
        """
        Initialize the ModelManager with a specified model.

        Args:
            model_name: The name of the Hugging Face model to use
        """
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.pipelines = {}

        # Check if transformers is available
        if not TRANSFORMERS_AVAILABLE:
            logger.warning("Transformers library not available. Using mock implementations.")
            return

        # Load the model and tokenizer
        self._load_model()

    def _load_model(self):
        """Load the model and tokenizer from Hugging Face."""
        # If transformers is not available, don't try to load the model
        if not TRANSFORMERS_AVAILABLE:
            logger.warning("Transformers library not available. Using mock implementations.")
            return

        try:
            logger.info(f"Loading model: {self.model_name}")

            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

            # Determine model type and load appropriate model
            # For simplicity, we're using a causal LM, but in a real app,
            # you might want to check the model type and load accordingly
            device_map = "auto" if TORCH_AVAILABLE and torch.cuda.is_available() else None
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                device_map=device_map
            )

            logger.info(f"Model {self.model_name} loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model {self.model_name}: {str(e)}")
            logger.info("Falling back to mock implementation")

    def _get_pipeline(self, task: str):
        """
        Get or create a pipeline for a specific task.

        Args:
            task: The task for the pipeline (e.g., 'text-generation', 'text-classification')

        Returns:
            A Hugging Face pipeline for the specified task
        """
        if not TRANSFORMERS_AVAILABLE:
            return None

        if task not in self.pipelines:
            try:
                device = 0 if TORCH_AVAILABLE and torch.cuda.is_available() else -1
                self.pipelines[task] = pipeline(
                    task,
                    model=self.model,
                    tokenizer=self.tokenizer,
                    device=device
                )
            except Exception as e:
                logger.error(f"Error creating pipeline for task {task}: {str(e)}")
                return None

        return self.pipelines[task]

    def generate_text(self, prompt: str, max_length: int = 100) -> str:
        """
        Generate text based on a prompt.

        Args:
            prompt: The input prompt for text generation
            max_length: Maximum length of generated text

        Returns:
            Generated text as a string
        """
        if not TRANSFORMERS_AVAILABLE or self.model is None:
            # Mock implementation for when the model isn't available
            return f"This is a mock response to: {prompt}"

        try:
            # Get the text generation pipeline
            generator = self._get_pipeline("text-generation")

            if generator is None:
                return f"Unable to generate text for: {prompt}"

            # Generate text
            result = generator(
                prompt,
                max_length=max_length,
                num_return_sequences=1,
                do_sample=True,
                temperature=0.7
            )

            # Extract and return the generated text
            generated_text = result[0]["generated_text"]

            # Remove the prompt from the beginning if it's there
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()

            return generated_text
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            return f"Error generating response for: {prompt}"

    def classify_text(self, text: str, labels: Optional[List[str]] = None) -> Dict[str, float]:
        """
        Classify text into predefined categories.

        Args:
            text: The text to classify
            labels: Optional list of labels for zero-shot classification

        Returns:
            Dictionary mapping labels to confidence scores
        """
        if not TRANSFORMERS_AVAILABLE or self.model is None:
            # Mock implementation
            if labels:
                import random
                return {label: random.random() for label in labels}
            return {"category1": 0.7, "category2": 0.2, "category3": 0.1}

        try:
            if labels:
                # Zero-shot classification
                classifier = self._get_pipeline("zero-shot-classification")
                if classifier is None:
                    # Fall back to mock implementation
                    import random
                    return {label: random.random() for label in labels}

                result = classifier(text, candidate_labels=labels)
                return dict(zip(result["labels"], result["scores"]))
            else:
                # Standard classification
                classifier = self._get_pipeline("text-classification")
                if classifier is None:
                    # Fall back to mock implementation
                    return {"category1": 0.7, "category2": 0.2, "category3": 0.1}

                result = classifier(text)
                return {r["label"]: r["score"] for r in result}
        except Exception as e:
            logger.error(f"Error classifying text: {str(e)}")
            # Fall back to mock implementation
            if labels:
                import random
                return {label: random.random() for label in labels}
            return {"category1": 0.7, "category2": 0.2, "category3": 0.1}

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.

        Returns:
            Dictionary with model information
        """
        device = "mock"
        if TORCH_AVAILABLE:
            device = "cuda" if torch.cuda.is_available() else "cpu"

        return {
            "model_name": self.model_name,
            "is_loaded": self.model is not None,
            "device": device,
            "transformers_available": TRANSFORMERS_AVAILABLE,
            "torch_available": TORCH_AVAILABLE
        }
