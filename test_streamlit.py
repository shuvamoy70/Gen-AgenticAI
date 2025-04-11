"""
Test Streamlit App for Network AI Assistant
"""
import streamlit as st

def main():
    """
    Simple test Streamlit app
    """
    st.set_page_config(
        page_title="Network AI Assistant - Test",
        page_icon="🌐",
        layout="wide"
    )
    
    st.title("🌐 Network AI Assistant - Test App")
    st.write("This is a test app to verify that Streamlit is working correctly.")
    
    st.subheader("Test Form")
    user_input = st.text_area("Enter a network issue:", "High latency in my network")
    
    if st.button("Submit"):
        st.success("Form submitted successfully!")
        st.write(f"You entered: {user_input}")
        
        with st.expander("Sample Response"):
            st.write("""
            Based on your description of high latency in your network, here are some possible causes:
            
            1. Network congestion
            2. Insufficient bandwidth
            3. Routing issues
            
            Recommended actions:
            - Check for bandwidth-intensive applications
            - Implement QoS (Quality of Service) policies
            - Optimize routing tables
            """)

if __name__ == "__main__":
    main()
