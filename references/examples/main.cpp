#include "Rectangle.hpp"
#include <iostream>
#include <memory>

int main() {
    std::cout << "--- Starting C++ Program ---\n";
    std::cout << "Initial tracking count: " << Geometry::Rectangle::getTotalRectangles() << "\n\n";

    // 1. Instantiating a stack-allocated object
    Geometry::Rectangle rect1(5.0, 3.5, "Custom Stack Rectangle");
    rect1.printDetails();

    // 2. Instantiating a modern, dynamic heap object using smart pointers (RAII compliant)
    auto rect2 = std::make_unique<Geometry::Rectangle>(10.0, 10.0, "Large Square");
    rect2->printDetails();

    // Check count with both objects alive
    std::cout << "Active objects in memory: " << Geometry::Rectangle::getTotalRectangles() << "\n\n";

    // Modifying values using setters
    std::cout << "--- Modifying Stack Rectangle Dimensions ---\n";
    rect1.setDimensions(7.0, 4.0);
    rect1.printDetails();

    // Smart pointer 'rect2' automatically frees memory here out of scope
    return 0;
}
