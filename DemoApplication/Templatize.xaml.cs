using DemoApplication.Class;
using IronPython.Hosting;
using Microsoft.Scripting.Hosting;
using System;
using System.Collections.Generic;
using System.Windows;

namespace DemoApplication
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        Templatizer python = new Templatizer();

        public MainWindow()
        {
            InitializeComponent();
        }

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            // Loading Projects
            //MessageBox.Show(python.CreateProject("Hello Universe", "Test Project that comes with the framework !"));
            //MessageBox.Show(python.CreateTemplate("Hello Universe", "Test1", "Dummy", 2));
            //MessageBox.Show(python.CreateTemplate("Hello Universe", "Test2", "Dummy", 7));
            //MessageBox.Show(python.CreateTemplate("Hello Universe", "Test3", "Dummy", 6));
            //MessageBox.Show(python.CreateTemplate("Hello Universe", "Test4", "Dummy", 1));
            //MessageBox.Show(python.CreateTemplate("Hello Universe", "Test5", "Dummy", 4));
            //MessageBox.Show(python.CreateTemplate("Hello Universe", "Test6", "Dummy", 1));
            MessageBox.Show(python.CreateModule("Hello Universe", "Test2", "King", "First module", 10, "a;sldkfjauherpiuhaweiguvnwienvpw"));
        }

        private void B_CreateProject_Click(object sender, RoutedEventArgs e)
        {
            
        }
    }
}
