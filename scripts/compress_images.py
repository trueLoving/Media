#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片压缩脚本
自动压缩images目录下的所有图片文件
支持格式：JPG, JPEG, PNG
支持并发压缩，提高处理速度
"""

import os
import sys
from PIL import Image
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from datetime import datetime
import shutil

# 线程锁，用于同步输出
print_lock = threading.Lock()

def compress_image(input_path, output_path, quality=85, max_size=(1920, 1080), min_compression_ratio=0):
    """
    压缩单个图片文件
    
    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
        quality: 压缩质量 (1-100)
        max_size: 最大尺寸 (宽, 高)
        min_compression_ratio: 最小压缩率要求 (百分比)
    """
    try:
        with Image.open(input_path) as img:
            # 转换为RGB模式（如果是RGBA，去除透明通道）
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # 调整尺寸（如果图片太大）
            original_size = img.size
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 保存压缩后的图片
            img.save(output_path, quality=quality, optimize=True)
            
            # 计算压缩率
            original_file_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            compression_ratio = (1 - compressed_size / original_file_size) * 100
            
            # 判断是否需要压缩
            if compression_ratio <= min_compression_ratio:
                # 压缩率不满足要求，删除压缩文件，复制原文件
                os.remove(output_path)
                shutil.copy2(input_path, output_path)
                
                with print_lock:
                    if compression_ratio <= 0:
                        print(f"⚠️  {os.path.basename(input_path)} -> {os.path.basename(output_path)} (跳过压缩)")
                        print(f"  原始大小: {original_file_size / 1024:.1f} KB")
                        print(f"  压缩后: {original_file_size / 1024:.1f} KB (保持原文件)")
                        print(f"  原因: 压缩后文件变大，保留原文件")
                    else:
                        print(f"⚠️  {os.path.basename(input_path)} -> {os.path.basename(output_path)} (跳过压缩)")
                        print(f"  原始大小: {original_file_size / 1024:.1f} KB")
                        print(f"  压缩后: {compressed_size / 1024:.1f} KB")
                        print(f"  压缩率: {compression_ratio:.1f}% (低于阈值 {min_compression_ratio}%)")
                        print(f"  原因: 压缩率不满足要求，保留原文件")
                    print()
                
                return True, input_path, original_file_size, original_file_size, 0
            else:
                # 正常压缩
                with print_lock:
                    print(f"✓ {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
                    print(f"  原始大小: {original_file_size / 1024:.1f} KB")
                    print(f"  压缩后: {compressed_size / 1024:.1f} KB")
                    print(f"  压缩率: {compression_ratio:.1f}%")
                    if original_size != img.size:
                        print(f"  尺寸调整: {original_size[0]}x{original_size[1]} -> {img.size[0]}x{img.size[1]}")
                    print()
                
                return True, input_path, original_file_size, compressed_size, compression_ratio
            
    except Exception as e:
        with print_lock:
            print(f"✗ 压缩失败 {os.path.basename(input_path)}: {str(e)}")
        return False, input_path, 0, 0, 0

def get_image_files(directory):
    """获取目录下的所有图片文件"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    image_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if Path(file).suffix.lower() in image_extensions:
                image_files.append(os.path.join(root, file))
    
    return image_files

def compress_images_concurrent(image_files, output_dir, quality, max_size, max_workers=4, overwrite=False, min_compression_ratio=0):
    """
    并发压缩图片文件
    
    Args:
        image_files: 图片文件列表
        output_dir: 输出目录
        quality: 压缩质量
        max_size: 最大尺寸
        max_workers: 最大工作线程数
        overwrite: 是否覆盖原文件
        min_compression_ratio: 最小压缩率要求
    """
    results = []
    total_original_size = 0
    total_compressed_size = 0
    
    print(f"开始并发压缩，使用 {max_workers} 个线程...")
    if min_compression_ratio > 0:
        print(f"最小压缩率要求: {min_compression_ratio}%")
    print("-" * 50)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有压缩任务
        future_to_path = {}
        for image_path in image_files:
            if overwrite:
                output_path = image_path
            else:
                relative_path = os.path.relpath(image_path, 'images')
                output_path = os.path.join(output_dir, relative_path)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            future = executor.submit(compress_image, image_path, output_path, quality, max_size, min_compression_ratio)
            future_to_path[future] = (image_path, output_path)
        
        # 处理完成的任务
        for future in as_completed(future_to_path):
            image_path, output_path = future_to_path[future]
            try:
                success, _, original_size, compressed_size, compression_ratio = future.result()
                if success:
                    results.append((True, image_path, original_size, compressed_size, compression_ratio))
                    total_original_size += original_size
                    total_compressed_size += compressed_size
                else:
                    results.append((False, image_path, 0, 0, 0))
            except Exception as e:
                with print_lock:
                    print(f"✗ 处理异常 {os.path.basename(image_path)}: {str(e)}")
                results.append((False, image_path, 0, 0, 0))
    
    return results, total_original_size, total_compressed_size

def main():
    parser = argparse.ArgumentParser(description='图片压缩工具 - 支持并发处理')
    parser.add_argument('--input', '-i', default='images', 
                       help='输入目录 (默认: images)')
    parser.add_argument('--output', '-o', default='images/compressed', 
                       help='输出目录 (默认: images/compressed)')
    parser.add_argument('--quality', '-q', type=int, default=85, 
                       help='压缩质量 1-100 (默认: 85)')
    parser.add_argument('--max-width', type=int, default=1920, 
                       help='最大宽度 (默认: 1920)')
    parser.add_argument('--max-height', type=int, default=1080, 
                       help='最大高度 (默认: 1080)')
    parser.add_argument('--overwrite', action='store_true', 
                       help='覆盖原文件')
    parser.add_argument('--workers', '-w', type=int, default=4,
                       help='并发工作线程数 (默认: 4)')
    parser.add_argument('--min-compression', type=float, default=0.0,
                       help='最小压缩率要求，低于此值将跳过压缩 (默认: 0.0%%)')
    
    args = parser.parse_args()
    
    # 检查输入目录是否存在
    if not os.path.exists(args.input):
        print(f"错误: 输入目录 '{args.input}' 不存在")
        sys.exit(1)
    
    # 创建输出目录
    if not args.overwrite:
        os.makedirs(args.output, exist_ok=True)
    
    # 获取所有图片文件
    image_files = get_image_files(args.input)
    
    if not image_files:
        print(f"在目录 '{args.input}' 中没有找到图片文件")
        sys.exit(0)
    
    print(f"找到 {len(image_files)} 个图片文件")
    print(f"压缩质量: {args.quality}")
    print(f"最大尺寸: {args.max_width}x{args.max_height}")
    print(f"输出目录: {args.output}")
    print(f"并发线程数: {args.workers}")
    if args.min_compression > 0:
        print(f"最小压缩率要求: {args.min_compression}%")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    # 并发压缩图片
    start_time = datetime.now()
    results, total_original_size, total_compressed_size = compress_images_concurrent(
        image_files, args.output, args.quality, 
        (args.max_width, args.max_height), args.workers, args.overwrite, args.min_compression
    )
    end_time = datetime.now()
    
    # 统计结果
    success_count = sum(1 for success, _, _, _, _ in results if success)
    total_count = len(results)
    
    # 统计压缩效果
    compressed_files = sum(1 for success, _, _, _, ratio in results if success and ratio > 0)
    skipped_files = sum(1 for success, _, _, _, ratio in results if success and ratio == 0)
    
    print("-" * 50)
    print(f"压缩完成! 成功: {success_count}/{total_count}")
    print(f"实际压缩: {compressed_files} 个文件")
    print(f"跳过压缩: {skipped_files} 个文件")
    print(f"总原始大小: {total_original_size / 1024 / 1024:.1f} MB")
    print(f"总压缩后大小: {total_compressed_size / 1024 / 1024:.1f} MB")
    if total_original_size > 0:
        overall_compression_ratio = (1 - total_compressed_size / total_original_size) * 100
        print(f"总体压缩率: {overall_compression_ratio:.1f}%")
    print(f"处理时间: {end_time - start_time}")
    
    if not args.overwrite:
        print(f"压缩后的文件保存在: {args.output}")
    
    # 显示压缩策略说明
    if args.min_compression > 0:
        print(f"\n💡 压缩策略: 只压缩压缩率超过 {args.min_compression}% 的文件")
        print("   其他文件将保持原样，确保压缩效果")
    else:
        print(f"\n💡 压缩策略: 压缩所有文件，即使压缩后文件变大")
        print("   建议设置 --min-compression 参数来优化压缩效果")

if __name__ == "__main__":
    main() 